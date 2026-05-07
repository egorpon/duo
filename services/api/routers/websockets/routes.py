import logging
from typing import Any, MutableMapping

from fastapi import APIRouter, WebSocket
from fastapi.websockets import WebSocketDisconnect

from generated import game_pb2, game_pb2_grpc
from services.api.routers.websockets.types import (
    AuthenticatedMessage,
    AuthenticatedMessageBody,
    DisconnectedMessage,
    DisconnectedMessageBody,
    GameMessage,
    GameMessageAdapter,
    MessageType,
)
from services.api.token import get_user_from_token

router = APIRouter(tags=['websocket'])

_logger = logging.getLogger('duo.api.websockets')


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

connections: dict[int, WebSocket] = {}


def get_opponent(game: game_pb2.Game, user: int) -> int:
    if game.player1 == user:
        return game.player2
    if game.player2 == user:
        return game.player1

    raise Exception('Opponent not found')


@router.websocket('/games/{game_id}/')
async def play_game(
    websocket: WebSocket,
    game_id: int,
) -> None:
    user: int | None = None
    logger.extra = {'game': game_id}

    game_service: game_pb2_grpc.GameServiceAsyncStub = (  # pyright: ignore
        game_pb2_grpc.GameServiceStub(websocket.app.state.game_channel)
    )
    try:
        game = await game_service.GetGameById(
            game_pb2.GetGameByIdRequest(game_id=game_id)
        )
        logger.debug('game present')
    except Exception:
        logger.debug('game not found')
        await websocket.close(reason='not found')
        return

    try:
        await websocket.accept()
        logger.debug('connection accepted')

        message = GameMessageAdapter.validate_json(
            await websocket.receive_json()
        )
        if message.type != MessageType.TOKEN:
            await websocket.close(code=1008, reason='not authenticated')
            return

        user = get_user_from_token(message.body.token)
        if user is None:
            await websocket.close(code=1008, reason='not authenticated')
            return

        logger.extra['user'] = user
        logger.debug('user verified')

        is_first_player_connects = game.player1 == user and game.player2 == 0
        is_second_player_joins = game.player1 != user and game.player2 == 0
        is_player_reconnected = user in [game.player1, game.player2]

        if not any(
            [
                is_first_player_connects,
                is_second_player_joins,
                is_player_reconnected,
            ]
        ):
            logger.debug('player does not belong to a game')
            await websocket.close()
            return

        connections[user] = websocket
        await websocket.send_json(
            data=AuthenticatedMessage(
                body=AuthenticatedMessageBody(
                    success=True,
                    message='Successfully authenticated',
                ),
            ).model_dump_json(),
        )

        if is_first_player_connects:
            pass

        elif is_second_player_joins:
            response = await game_service.JoinGame(
                game_pb2.JoinGameRequest(game_id=game.id, player_id=user),
            )
            game = response.game

        elif is_player_reconnected:
            pass

        while True:
            message = GameMessageAdapter.validate_json(
                await websocket.receive_json()
            )
            logger.debug('message received: %s', message)

    except WebSocketDisconnect:
        logger.debug('user disconnected')
    except Exception:
        logger.exception('Unexpected exception')
    finally:
        if user:
            opponent = get_opponent(game=game, user=user)
            if opponent in connections.keys():
                await connections[opponent].send_json(
                    data=DisconnectedMessage(
                        body=DisconnectedMessageBody(
                            message='Opponent disconnected'
                        ),
                    ).model_dump_json(),
                )
                connections.pop(user, None)
