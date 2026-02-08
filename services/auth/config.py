from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_PATH = Path(__file__).parent


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_PATH / '.env',
        extra='ignore',
    )
    secret_key: SecretStr = Field(alias='duo_auth_secret_key')
    jwt_lifetime: int = 60 * 60 * 24 * 30  # 30 days
    jwt_algorithm: str = 'HS256'


settings = AuthSettings()  # pyright: ignore[reportCallIssue]
