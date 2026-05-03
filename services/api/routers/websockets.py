import json
import logging
from typing import Any, Mapping

from fastapi import APIRouter, WebSocket
from fastapi.websockets import WebSocketDisconnect

logger = logging.getLogger('duo.api.websockets')

router = APIRouter(tags=['websocket'])


class WebSocketManager:
    def __init__(self) -> None:
        self.connections: list[WebSocket] = []

    def add_connection(self, socket: WebSocket) -> None:
        self.connections.append(socket)

    def remove_connection(self, socket: WebSocket) -> None:
        self.connections.remove(socket)

    async def send_all(self, message: Mapping[str, Any]) -> None:
        for connection in self.connections:
            try:
                await connection.send_json(message)
            except Exception:
                logger.exception('failed to send message to %s', connection)
                pass


manager = WebSocketManager()


@router.websocket('/games/{game_id}/')
async def play_game(websocket: WebSocket, game_id: int) -> None:
    logger.debug('game %s: got connection', game_id)
    try:
        await websocket.accept()
        manager.add_connection(websocket)
        logger.debug('game %s: accepted ws connection', game_id)
        await manager.send_all({'message': 'someone new'})
        while True:
            logger.debug('waiting for message')
            data = await websocket.receive()
            if data.get('type') == 'websocket.disconnect':
                logger.debug('client disconnected')
                return

            logger.debug('received message: %s', data)
            text: str = data.get('text', '')
            await manager.send_all({'message': text})

    except WebSocketDisconnect:
        logger.exception('Client disconnected')
    except Exception:
        logger.exception('Unexpected exception')
    finally:
        manager.remove_connection(websocket)
        await manager.send_all({'message': 'someone left'})
