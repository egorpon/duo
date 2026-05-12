import json
import logging
from typing import Any, MutableMapping

from fastapi import APIRouter, WebSocket
from fastapi.websockets import WebSocketDisconnect

from generated import game_pb2, game_pb2_grpc
from services.api.routers.websockets.types import (
    AuthenticatedMessage,
    AuthenticatedMessageBody,
    ConnectedMessage,
    ConnectedMessageBody,
    DisconnectedMessage,
    DisconnectedMessageBody,
    GameMessageAdapter,
    GameStateMessage,
    GameStateMessageBody,
    InvalidMoveMessage,
    InvalidMoveMessageBody,
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

        game = self.extra.get('game', '-')
        user = self.extra.get('user', '-')
        return f'({game} : {user}) {msg}', kwargs


connections: dict[int, WebSocket] = {}


def get_opponent(game: game_pb2.Game, user: int) -> int | None:
    if game.player1 == user:
        return game.player2
    if game.player2 == user:
        return game.player1
    return None


async def handle_authentication(
    *,
    websocket: WebSocket,
    logger: GameLoggingAdapter,
) -> int | None:
    await websocket.accept()
    logger.debug('connection accepted')

    message = GameMessageAdapter.validate_python(await websocket.receive_json())

    if message.type != MessageType.TOKEN:
        logger.debug('received message is not token, rejecting')
        await websocket.close(code=1008, reason='not authenticated')
        return None

    user = get_user_from_token(message.body.token)
    if user is None:
        logger.debug('token is not valid, rejecting')
        await websocket.close(code=1008, reason='not authenticated')
        return None

    return user


async def _game_loop(
    *,
    logger: GameLoggingAdapter,
    websocket: WebSocket,
    game_service: game_pb2_grpc.GameServiceAsyncStub,
    user: int,
    game_id: int,
) -> None:
    while True:
        logger.debug('waiting for message')
        message = GameMessageAdapter.validate_python(
            await websocket.receive_json()
        )
        logger.debug('message received: %s', message)
        if message.type != MessageType.GAME_MOVE:
            await websocket.send_text(
                InvalidMoveMessage(
                    body=InvalidMoveMessageBody(message='invalid move')
                ).model_dump_json()
            )
            continue
        try:
            move_response = await game_service.MakeMove(
                game_pb2.MakeMoveRequest(
                    game_id=game_id,
                    player_id=user,
                    move_data=json.dumps(message.body.game_move),
                )
            )
        except Exception:
            await websocket.send_text(
                InvalidMoveMessage(
                    body=InvalidMoveMessageBody(message='invalid move')
                ).model_dump_json()
            )
            continue

        game = move_response.game
        await connections[game.player1].send_text(
            GameStateMessage(
                body=GameStateMessageBody(
                    game_state=json.loads(move_response.player1_view)
                )
            ).model_dump_json()
        )
        await connections[game.player2].send_text(
            GameStateMessage(
                body=GameStateMessageBody(
                    game_state=json.loads(move_response.player2_view)
                )
            ).model_dump_json()
        )


async def _fetch_game(
    *,
    game_service: game_pb2_grpc.GameServiceAsyncStub,
    game_id: int,
) -> game_pb2.Game | None:
    try:
        return await game_service.GetGameById(
            game_pb2.GetGameByIdRequest(game_id=game_id)
        )
    except Exception:
        return None


@router.websocket('/games/{game_id}/')
async def play_game(
    websocket: WebSocket,
    game_id: int,
) -> None:
    user: int | None = None
    logger = GameLoggingAdapter(logger=_logger)
    logger.extra = {'game': game_id}

    game_service: game_pb2_grpc.GameServiceAsyncStub = (  # pyright: ignore
        game_pb2_grpc.GameServiceStub(websocket.app.state.game_channel)
    )
    game = await _fetch_game(game_service=game_service, game_id=game_id)
    if not game:
        await websocket.close()
        return

    try:
        user = await handle_authentication(websocket=websocket, logger=logger)
        if not user:
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
        await websocket.send_text(
            data=AuthenticatedMessage(
                body=AuthenticatedMessageBody(
                    success=True,
                    message='Successfully authenticated',
                ),
            ).model_dump_json(),
        )

        if is_first_player_connects:
            logger.debug('first player connected, waiting for second player')

        elif is_second_player_joins:
            logger.debug('second player joins game')
            response = await game_service.JoinGame(
                game_pb2.JoinGameRequest(game_id=game.id, player_id=user),
            )
            game = response.game
            await connections[game.player1].send_text(
                GameStateMessage(
                    body=GameStateMessageBody(
                        game_state=json.loads(response.player1_view)
                    )
                ).model_dump_json()
            )
            await connections[game.player2].send_text(
                GameStateMessage(
                    body=GameStateMessageBody(
                        game_state=json.loads(response.player2_view)
                    )
                ).model_dump_json()
            )

        elif is_player_reconnected:
            logger.debug('second player is reconnected, can safely play a game')
            player_view = await game_service.GetPlayerView(
                game_pb2.GetPlayerViewRequest(game_id=game.id, player_id=user)
            )
            await connections[user].send_text(
                GameStateMessage(
                    body=GameStateMessageBody(
                        game_state=json.loads(player_view.game_state)
                    )
                ).model_dump_json()
            )
            opponent = get_opponent(game=game, user=user)
            if opponent and opponent in connections:
                await connections[opponent].send_text(
                    ConnectedMessage(
                        body=ConnectedMessageBody(
                            message=f'Opponent {user} connected'
                        ),
                    ).model_dump_json()
                )
                logger.debug('second player connected')
            else:
                logger.debug('player reconnected to empty room')

        await _game_loop(
            logger=logger,
            user=user,
            websocket=websocket,
            game_id=game_id,
            game_service=game_service,
        )
    except WebSocketDisconnect:
        logger.debug('user disconnected')
    except Exception:
        logger.exception('Unexpected exception')
    finally:
        if user:
            connections.pop(user, None)
            opponent = get_opponent(game=game, user=user)
            if opponent:
                await connections[opponent].send_text(
                    data=DisconnectedMessage(
                        body=DisconnectedMessageBody(
                            message='Opponent disconnected'
                        ),
                    ).model_dump_json(),
                )
