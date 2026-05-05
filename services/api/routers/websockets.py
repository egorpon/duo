import enum
import logging
from typing import Annotated, Any, Literal, Mapping, MutableMapping, Union

from fastapi import APIRouter, WebSocket
from fastapi.websockets import WebSocketDisconnect
from pydantic import BaseModel, Field, TypeAdapter

from services.api.token import get_user_from_token

_logger = logging.getLogger('duo.api.websockets')


class MessageType(str, enum.Enum):
    AUTHENTICATED = 'authenticated'
    GAME_MOVE = 'game_move'
    GAME_STATE = 'game_state'
    GAME_CREATED = 'game_created'
    CONNECTED = 'connected'
    DISCONNECTED = 'disconnected'
    INVALID_MOVE = 'invalid_move'


class AuthenticatedMessageBody(BaseModel):
    message: str
    success: bool


class ConnectedMessageBody(BaseModel):
    message: str


class DisconnectedMessageBody(BaseModel):
    message: str


class GameMoveMessageBody(BaseModel):
    game_move: Mapping[Any, Any]


class GameCreatedMessageBody(BaseModel):
    message: str


class GameStateMessageBody(BaseModel):
    game_state: Mapping[Any, Any]


class InvalidMoveMessageBody(BaseModel):
    message: str


class AuthenticatedMessage(BaseModel):
    type: Literal[MessageType.AUTHENTICATED] = MessageType.AUTHENTICATED
    body: AuthenticatedMessageBody


class ConnectedMessage(BaseModel):
    type: Literal[MessageType.CONNECTED] = MessageType.CONNECTED
    body: ConnectedMessageBody


class DisconnectedMessage(BaseModel):
    type: Literal[MessageType.DISCONNECTED] = MessageType.DISCONNECTED
    body: DisconnectedMessageBody


class GameMoveMessage(BaseModel):
    type: Literal[MessageType.GAME_MOVE] = MessageType.GAME_MOVE
    body: GameMoveMessageBody


class GameCreatedMessage(BaseModel):
    type: Literal[MessageType.GAME_CREATED] = MessageType.GAME_CREATED
    body: GameCreatedMessageBody


class GameStateMessage(BaseModel):
    type: Literal[MessageType.GAME_STATE] = MessageType.GAME_STATE
    body: GameStateMessageBody


class InvalidMoveMessage(BaseModel):
    type: Literal[MessageType.INVALID_MOVE] = MessageType.INVALID_MOVE
    body: InvalidMoveMessageBody


GameMessage = Annotated[
    Union[
        AuthenticatedMessage,
        ConnectedMessage,
        DisconnectedMessage,
        GameMoveMessage,
        GameCreatedMessage,
        GameStateMessage,
        InvalidMoveMessage,
    ],
    Field(discriminator='type'),
]
GameMessageAdapter = TypeAdapter[GameMessage](GameMessage)


class GameLoggingAdapter(logging.LoggerAdapter[logging.Logger]):
    def process(
        self, msg: Any, kwargs: MutableMapping[str, Any]
    ) -> tuple[Any, MutableMapping[str, Any]]:
        if self.extra is None:
            return msg, kwargs

        game = self.extra.get('game', '_')
        user = self.extra.get('user', '_')
        return f'({game} : {user}) {msg}', kwargs


logger = GameLoggingAdapter(logger=_logger)

router = APIRouter(tags=['websocket'])

MAX_PLAYERS = 2


class WebSocketManager:
    connections: dict[int, dict[int, WebSocket]]

    def __init__(self, logger: logging.LoggerAdapter[logging.Logger]) -> None:
        self.connections = {}
        self.log = logger

    def add_connection(
        self,
        *,
        game: int,
        player: int,
        socket: WebSocket,
    ) -> None:
        if game not in self.connections:
            self.connections[game] = {player: socket}
            return

        if len(self.connections[game]) >= MAX_PLAYERS:
            raise Exception('max players, cant connect')

        if player not in self.connections[game]:
            self.connections[game][player] = socket
            return

        raise Exception('cannot connect, already connected')

    def _get_opponent(self, game: int, player: int) -> WebSocket | None:
        if game not in self.connections:
            return None

        for player_id, websocket in self.connections[game].items():
            if player_id == player:
                continue
            return websocket

    def remove_connection(
        self,
        *,
        game: int,
        player: int,
    ) -> None:
        if game not in self.connections or player not in self.connections[game]:
            return

        self.connections[game].pop(player)
        if not self.connections[game]:
            self.connections.pop(game)

    async def message_players(self, *, game: int, message: GameMessage) -> None:
        if game not in self.connections:
            return
        for ws in self.connections[game].values():
            try:
                await ws.send_json(message.model_dump_json())
            except Exception:
                self.log.exception('failed to send message')

    async def message_player(
        self, *, game: int, player: int, message: GameMessage
    ) -> None:
        if game not in self.connections or player not in self.connections[game]:
            return

        try:
            await self.connections[game][player].send_json(
                message.model_dump_json()
            )
        except Exception:
            self.log.exception('failed to send message')

    async def message_opponent(
        self, *, game: int, player: int, message: GameMessage
    ) -> None:
        ws = self._get_opponent(game=game, player=player)
        if not ws:
            return
        try:
            await ws.send_json(message.model_dump_json())
        except Exception:
            self.log.exception('failed to send message')


manager = WebSocketManager(logger=logger)


@router.websocket('/games/{game}/')
async def play_game(
    websocket: WebSocket,
    game: int,
) -> None:
    user: int | None = None
    logger.extra = {'game': game}
    try:
        await websocket.accept()
        logger.debug('connection accepted')

        message = await websocket.receive_json()
        user = get_user_from_token(message.get('token', ''))
        if user is None:
            await websocket.close(code=1008, reason='not authenticated')
            return

        logger.extra['user'] = user
        logger.debug('user verified')
        manager.add_connection(game=game, player=user, socket=websocket)
        await manager.message_player(
            game=game,
            player=user,
            message=AuthenticatedMessage(
                body=AuthenticatedMessageBody(
                    success=True,
                    message='Successfully authenticated',
                ),
            ),
        )
        await manager.message_opponent(
            game=game,
            player=user,
            message=ConnectedMessage(
                body=ConnectedMessageBody(
                    message='Opponent connected',
                ),
            ),
        )
        while True:
            data = await websocket.receive_json()
            logger.debug('received message: %s', data)
            text: str = data.get('message', '')
            await manager.message_opponent(
                game=game,
                player=user,
                message=GameMoveMessage(
                    body=GameMoveMessageBody(game_move={'message': text}),
                ),
            )

    except WebSocketDisconnect:
        logger.debug('user disconnected')
    except Exception:
        logger.exception('Unexpected exception')
    finally:
        if user:
            await manager.message_opponent(
                game=game,
                player=user,
                message=DisconnectedMessage(
                    body=DisconnectedMessageBody(
                        message='Opponent disconnected'
                    ),
                ),
            )
            manager.remove_connection(game=game, player=user)
