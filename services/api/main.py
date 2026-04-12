from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from grpc import aio

from services.api.config import settings
from services.api.routers.auth import router as auth_router
from services.api.routers.games import router as games_router
from services.api.routers.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.auth_channel = aio.insecure_channel(
        str(settings.auth_service_url)
    )
    app.state.game_channel = aio.insecure_channel(
        str(settings.game_service_url)
    )

    yield

    await app.state.auth_channel.close()
    await app.state.game_channel.close()


app = FastAPI(
    title='Duo API',
    version='v0.0.1',
    root_path='/api/v1',
)
app.include_router(auth_router, prefix='/auth')
app.include_router(users_router, prefix='/users')
app.include_router(games_router, prefix='/games')


@app.get('/', tags=['status'])
def main() -> dict[str, Any]:
    return {'status': 'ok'}
