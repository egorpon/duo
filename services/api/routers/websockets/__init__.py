from fastapi import APIRouter
from fastapi.websockets import WebSocketDisconnect

from fastapi import WebSocket

from services.api.token import get_user_from_token

from .manager import logger, manager
from .types import (
    AuthenticatedMessage,
    AuthenticatedMessageBody,
    ConnectedMessage,
    ConnectedMessageBody,
    DisconnectedMessage,
    DisconnectedMessageBody,
    GameMoveMessage,
    GameMoveMessageBody,
)

router = APIRouter(tags=['websocket'])


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
