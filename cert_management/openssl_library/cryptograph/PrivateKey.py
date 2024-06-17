from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey


class PrivateKey:

    def convert_to_file(self, private_key: RSAPrivateKey, public_key: RSAPublicKey, passphrase: str = None) -> tuple[bytes, bytes]:
        encryption = serialization.BestAvailableEncryption(
            passphrase.encode()) if passphrase else serialization.NoEncryption()

        bytes_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=encryption
        )

        bytes_public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return bytes_private_key, bytes_public_key

    def create_private_key(self, passphrase: str = None) -> tuple[RSAPrivateKey, RSAPublicKey]:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        return private_key, public_key
