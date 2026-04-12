from pathlib import Path

from pydantic import AnyHttpUrl, AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_PATH = Path(__file__).parent


class ApiSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_PATH / '.env',
        extra='ignore',
    )
    debug: bool = Field(alias='duo_api_debug')
    allowed_origins: list[AnyHttpUrl] = Field(alias='duo_allowed_origins')
    auth_service_url: AnyUrl = Field(alias='duo_auth_service_url')
    game_service_url: AnyUrl = Field(alias='duo_game_service_url')


settings = ApiSettings()  # pyright: ignore[reportCallIssue]
