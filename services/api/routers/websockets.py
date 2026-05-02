import logging

from fastapi import APIRouter, WebSocket
from fastapi.websockets import WebSocketDisconnect

logger = logging.getLogger('duo.api.websockets')

router = APIRouter(tags=['websocket'])


@router.websocket('/games/{game_id}/')
async def play_game(websocket: WebSocket, game_id: int) -> None:
    logger.debug('game %s: got connection', game_id)
    try:
        await websocket.accept()
        logger.debug('game %s: accepted ws connection', game_id)
        while True:
            logger.debug('waiting for message')
            data = await websocket.receive()
            if data.get('type') == 'websocket.disconnect':
                logger.debug('client disconnected')
                return
            logger.debug('received message: %s', data)
            logger.debug('sending reply')
            await websocket.send_json({'text': 'hello'})

    except WebSocketDisconnect:
        logger.exception('Client disconnected')
    except Exception:
        logger.exception('Unexpected exception')
