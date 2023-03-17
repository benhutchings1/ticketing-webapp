import os
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
PRIVATE_KEY_DIR = os.path.join(BASE_DIR, "private_key.pem")


def read_key_pair() -> Ed25519PrivateKey | None:
    try:
        with open(PRIVATE_KEY_DIR, "rb") as f:
            serialized_private = f.read()

        private_key = serialization.load_pem_private_key(
            serialized_private,
            password=None
        )

        return private_key

    except FileNotFoundError:
        return None


def create_key_pair() -> (Ed25519PublicKey, Ed25519PrivateKey):
    # Read key if exists
    private_key = read_key_pair()

    if private_key is None:
        # Generate key
        private_key = Ed25519PrivateKey.generate()

        # Serialize key
        serialized_private = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        # Write key
        with open(PRIVATE_KEY_DIR, "wb") as f:
            f.write(serialized_private)

    # Get public key
    public_key = private_key.public_key()

    return public_key, private_key


def sign_msg(msg: bytes, private_key: Ed25519PrivateKey) -> bytes:
    return private_key.sign(msg)


def verify_msg(msg: bytes, signature: bytes, public_key: Ed25519PublicKey) -> bool:
    try:
        public_key.verify(signature, msg)
        return True
    except InvalidSignature:
        return False
