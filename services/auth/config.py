from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from pydantic import Field, PostgresDsn, SecretStr, TypeAdapter
from pydantic_settings import BaseSettings, SettingsConfigDict

from common.secrets import load_private_key, load_public_key

BASE_PATH = Path(__file__).parent


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_PATH / '.env',
        extra='ignore',
    )
    private_key_path: Path = Field(alias='duo_auth_private_key_path')
    public_key_path: Path = Field(alias='duo_auth_public_key_path')
    jwt_lifetime: int = 60 * 60 * 24 * 30  # 30 days
    jwt_algorithm: str = 'EdDSA'

    db_host: str = Field(alias='postgres_host')
    db_port: str = Field(alias='postgres_port')
    db_name: str = Field(alias='postgres_db')
    db_user: str = Field(alias='postgres_user')
    db_pass: SecretStr = Field(alias='postgres_password')

    @property
    def db_dsn(self) -> PostgresDsn:
        dsn_str = (
            f'postgresql+asyncpg://'
            f'{self.db_user}:{self.db_pass.get_secret_value()}@'
            f'{self.db_host}:{self.db_port}/{self.db_name}'
        )
        return TypeAdapter(PostgresDsn).validate_strings(dsn_str)

    def get_private_key(self) -> Ed25519PrivateKey:
        return load_private_key(BASE_PATH / self.private_key_path)

    def get_public_key(self) -> Ed25519PublicKey:
        return load_public_key(BASE_PATH / self.public_key_path)


settings = AuthSettings()  # pyright: ignore[reportCallIssue]
