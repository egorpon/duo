from typing import Any

from fastapi import FastAPI, WebSocket
from fastapi.openapi.utils import get_openapi

from api.config import settings
from api.routers.auth import router as auth_router
from api.websockets import WebSocketsClient


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title='Duo API',
        version='1.0',
        routes=app.routes,
    )

    openapi_schema['components']['securitySchemes'] = {
        'BearerAuth': {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }
    }

    openapi_schema['security'] = [{'BearerAuth': []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI()
app.openapi = custom_openapi  # type: ignore
app.include_router(auth_router, prefix='/auth', tags=['auth'])


client = WebSocketsClient()


@app.get('/', tags=['status'])
def main() -> dict[str, Any]:
    print(settings)
    return {'message': 'ok'}


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
