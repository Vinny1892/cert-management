from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey


class PrivateKey:

    def convert_to_file(self, private_key: RSAPrivateKey, passphrase: str) -> bytes:
        encryption = serialization.BestAvailableEncryption(
            passphrase.encode()) if passphrase else serialization.NoEncryption()

        key_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=encryption
        )
        return key_bytes

    def create_private_key(self, passphrase) -> RSAPrivateKey:
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        # encryption = serialization.BestAvailableEncryption(
        #     passphrase.encode()) if passphrase else serialization.NoEncryption()
        #
        # key_bytes = key.private_bytes(
        #     encoding=serialization.Encoding.PEM,
        #     format=serialization.PrivateFormat.TraditionalOpenSSL,
        #     encryption_algorithm=encryption
        # )

        return key