from typing import Any

from fastapi import FastAPI, WebSocket

from services.api.routers.auth import router as auth_router
from services.api.routers.games import router as games_router
from services.api.routers.users import router as users_router
from services.api.websockets import WebSocketsClient

app = FastAPI(
    title='Duo API',
    version='v0.0.1',
    root_path='/api/v1',
)
app.include_router(auth_router, prefix='/auth')
app.include_router(users_router, prefix='/users')
app.include_router(games_router, prefix='/games')


client = WebSocketsClient()


@app.get('/', tags=['status'])
def main() -> dict[str, Any]:
    return {'status': 'ok'}


@app.websocket('/ws')
async def websocket_api(websocket: WebSocket) -> None:
    await client.connected(websocket)
    try:
        await client.notify_all(
            f'Someone new here. Now us {client.connections}'
        )
        while True:
            await websocket.receive()

    except Exception:
        await client.disconnected(websocket)
        await client.notify_all(f'Someone left us. {client.connections} left')
        return None
