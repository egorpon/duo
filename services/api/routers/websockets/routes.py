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

        message = await websocket.receive_json()
        user = get_user_from_token(message.get('token', ''))
        if user is None:
            await websocket.close(code=1008, reason='not authenticated')
            return

        logger.extra['user'] = user
        logger.debug('user verified')
        if not game.player2 and user != game.player1:
            join_result = await game_service.JoinGame(
                game_pb2.JoinGameRequest(game_id=game_id, player_id=user)
            )
            game = join_result.game

        elif game.player2 and user not in [game.player1, game.player2]:
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
