import logging
from typing import Any, Mapping

from fastapi import APIRouter, WebSocket
from fastapi.websockets import WebSocketDisconnect

from services.api.token import get_user_from_token

logger = logging.getLogger('duo.api.websockets')

router = APIRouter(tags=['websocket'])

MAX_PLAYERS = 2


class WebSocketManager:
    connections: dict[int, dict[int, WebSocket]]

    def __init__(self) -> None:
        self.connections = {}

    def add_connection(
        self,
        *,
        game: int,
        player: int,
        socket: WebSocket,
    ) -> None:
        if not self.connections.get(game):
            self.connections[game] = {player: socket}

        if len(self.connections[game]) >= MAX_PLAYERS:
            raise Exception('max players, cant connect')

        if not self.connections[game].get(player):
            self.connections[game][player] = socket

    def remove_connection(
        self,
        *,
        game: int,
        player: int,
    ) -> None:
        pass

    async def send_to_players(
        self,
        *,
        game: int,
        message: Mapping[str, Any],
    ) -> None:
        for connection in self.connections:
            try:
                pass
            except Exception:
                logger.exception('failed to send message to %s', connection)

    async def send_to_player(
        self,
        *,
        game: int,
        player: int,
        message: Mapping[str, Any],
    ) -> None:
        pass

    async def send_to_opponent(
        self,
        *,
        game: int,
        player: int,
        message: Mapping[str, Any],
    ) -> None:
        pass


manager = WebSocketManager()


@router.websocket('/games/{game}/')
async def play_game(
    websocket: WebSocket,
    game: int,
) -> None:
    user: int | None = None
    try:
        await websocket.accept()
        logger.debug('game %s: got connection', game)

        message = await websocket.receive_json()
        if message.get('type') == 'websocket.disconnect':
            logger.debug('client disconnected')
            return

        logger.debug('game %s: first message: %s', game, message)
        token: str = message.get('token', '')
        if not token:
            await websocket.close(code=1008, reason='not authenticated')
            return

        user = get_user_from_token(token)
        if user is None:
            await websocket.close(code=1008, reason='not authenticated')
            return

        logger.debug('game %s: verification passed, user %s', game, user)
        manager.add_connection(game=game, player=user, socket=websocket)
        while True:
            logger.debug('game %s: waiting for message', game)
            data = await websocket.receive()

            logger.debug('game %s: received message: %s', game, data)
            text: str = data.get('text', '')
            await manager.send_to_opponent(
                game=game, player=user, message={'message': text}
            )

    except WebSocketDisconnect:
        logger.exception('Client disconnected')
    except Exception:
        logger.exception('Unexpected exception')
    finally:
        if user:
            manager.remove_connection(game=game, player=user)
            await manager.send_to_opponent(
                game=game, player=user, message={'message': 'no opponent'}
            )
