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

        if len(self.connections[game]) < MAX_PLAYERS:
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

    async def message_players(
        self,
        *,
        game: int,
        message: Mapping[str, Any],
    ) -> None:
        if game not in self.connections:
            return
        for player_id, ws in self.connections[game].items():
            try:
                await ws.send_json(message)
            except Exception:
                logger.exception('failed to send message to %s', player_id)

    async def message_player(
        self,
        *,
        game: int,
        player: int,
        message: Mapping[str, Any],
    ) -> None:
        if game not in self.connections or player not in self.connections:
            return

        try:
            await self.connections[game][player].send_json(message)
        except Exception:
            logger.exception('failed to send message to %s', player)

    async def message_opponent(
        self,
        *,
        game: int,
        player: int,
        message: Mapping[str, Any],
    ) -> None:
        ws = self._get_opponent(game=game, player=player)
        if not ws:
            return
        try:
            await ws.send_json(message)
        except Exception:
            logger.exception('failed to send message to opponent of %s', player)


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
        logger.debug('manager state: %s', manager.connections)

        message = await websocket.receive_json()
        if message.get('type') == 'websocket.disconnect':
            logger.debug('game %s: disconnected', game)
            logger.debug('client disconnected')
            return

        user = get_user_from_token(message.get('token', ''))
        if user is None:
            await websocket.close(code=1008, reason='not authenticated')
            return

        logger.debug('game %s: verification passed, user %s', game, user)
        manager.add_connection(game=game, player=user, socket=websocket)
        await manager.message_opponent(
            game=game,
            player=user,
            message={'message': f'opponent {user} connected'},
        )
        logger.debug('added connection %s, %s, %s', game, user, websocket)
        while True:
            logger.debug('game %s: waiting for message', game)
            data = await websocket.receive_json()

            if message.get('type') == 'websocket.disconnect':
                await manager.message_opponent(
                    game=game, player=user, message={'message': 'opponent left'}
                )
                manager.remove_connection(game=game, player=user)
                logger.debug('game %s: disconnected', game)
                return

            logger.debug('game %s: received message: %s', game, data)
            text: str = data.get('message', '')
            await manager.message_opponent(
                game=game, player=user, message={'message': text}
            )

    except WebSocketDisconnect:
        logger.exception('Client disconnected')
    except Exception:
        logger.exception('Unexpected exception')
    finally:
        if user:
            manager.remove_connection(game=game, player=user)
            await manager.message_players(
                game=game, message={'message': f'player {user} disconnected'}
            )
