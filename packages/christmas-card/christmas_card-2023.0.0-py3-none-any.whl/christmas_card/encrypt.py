import base64
import inspect
from pathlib import Path

import typer
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import christmas_card


def derive_key(passphrase: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'probablyfinetoskipthismaybeidk',
        iterations=480000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(passphrase))


def encrypt(file_path: Path, passphrase: str):
    passphrase = passphrase.encode()
    key = derive_key(passphrase)
    f = Fernet(key)

    plaintext = file_path.read_bytes()
    module_path = Path(inspect.getfile(christmas_card))
    output_path = module_path.parent / "encrypted_card.md"

    output_path.write_bytes(f.encrypt(plaintext))


def decrypt(file_path: Path, passphrase: bytes) -> str:
    f = Fernet(derive_key(passphrase))
    encrypted = file_path.read_bytes()
    plaintext = f.decrypt(encrypted)
    return plaintext.decode()


if __name__ == "__main__":
    typer.run(encrypt)
