from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)


def load_private_key(location: Path) -> Ed25519PrivateKey:
    with open(location, 'rb') as f:
        key = serialization.load_pem_private_key(
            f.read(),
            password=None,
        )
        if not isinstance(key, Ed25519PrivateKey):
            raise TypeError('Expected Ed25519 private key')

        return key


def load_public_key(location: Path) -> Ed25519PublicKey:
    with open(location, 'rb') as f:
        key = serialization.load_pem_public_key(f.read())

        if not isinstance(key, Ed25519PublicKey):
            raise TypeError('Expected Ed25519 public key')

        return key
