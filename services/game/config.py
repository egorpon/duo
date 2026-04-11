import logging
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from pydantic import Field, PostgresDsn, SecretStr, TypeAdapter
from pydantic_settings import BaseSettings, SettingsConfigDict

from common.secrets import load_public_key

logger = logging.getLogger('duo.auth.config')

BASE_PATH = Path(__file__).parent


class GameSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_PATH / '.env',
        extra='ignore',
    )

    public_key_path: Path = Field(alias='duo_auth_public_key_path')

    db_host: str = Field(alias='postgres_host')
    db_port: str = Field(alias='postgres_port')
    db_name: str = Field(alias='postgres_db')
    db_user: str = Field(alias='postgres_user')
    db_pass: SecretStr = Field(alias='postgres_password')
    jwt_algorithm: str = 'EdDSA'

    _public_key: Ed25519PublicKey | None = None

    @property
    def db_dsn(self) -> PostgresDsn:
        dsn_str = (
            f'postgresql+asyncpg://'
            f'{self.db_user}:{self.db_pass.get_secret_value()}@'
            f'{self.db_host}:{self.db_port}/{self.db_name}'
        )
        return TypeAdapter(PostgresDsn).validate_strings(dsn_str)

    @property
    def public_key(self) -> Ed25519PublicKey:
        assert self._public_key is not None, 'Public key is not loaded properly'
        return self._public_key

    def model_post_init(self, context: Any, /) -> None:
        self._public_key = load_public_key(BASE_PATH / self.public_key_path)
        logger.debug('Loaded encryption keys successfully')


settings = GameSettings()  # pyright: ignore[reportCallIssue]
