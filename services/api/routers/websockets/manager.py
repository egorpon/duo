import logging
from typing import Any, MutableMapping

from fastapi import WebSocket

from services.api.exceptions import AlreadyConnectedError, ConnectionLimitError
from services.api.routers.websockets.types import GameMessage

_logger = logging.getLogger('duo.api.websockets')

MAX_PLAYERS = 2


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
            raise ConnectionLimitError('max players, cant connect')

        if player not in self.connections[game]:
            self.connections[game][player] = socket
            return

        raise AlreadyConnectedError('cannot connect, already connected')

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
