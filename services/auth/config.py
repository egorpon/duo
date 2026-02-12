from pathlib import Path

from pydantic import Field, PostgresDsn, SecretStr, TypeAdapter
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

    db_host: str = Field(alias='postgres_host')
    db_port: str = Field(alias='postgres_port')
    db_name: str = Field(alias='postgres_name')
    db_user: str = Field(alias='postgres_user')
    db_pass: SecretStr = Field(alias='postgres_password')

    @property
    def dsn(self) -> PostgresDsn:
        dsn_str = (
            f'postgresql+asyncpg://'
            f'{self.db_user}:{self.db_pass.get_secret_value()}@'
            f'{self.db_host}:{self.db_port}/{self.db_name}'
        )
        return TypeAdapter(PostgresDsn).validate_strings(dsn_str)



settings = AuthSettings()  # pyright: ignore[reportCallIssue]
