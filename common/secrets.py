from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.types import (
    PrivateKeyTypes,
    PublicKeyTypes,
)


def load_private_key(location: Path) -> PrivateKeyTypes:
    with open(location, 'rb') as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None,
        )


def load_public_key(location: Path) -> PublicKeyTypes:
    with open(location, 'rb') as f:
        return serialization.load_pem_public_key(f.read())
