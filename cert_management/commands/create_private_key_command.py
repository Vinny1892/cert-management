from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

from cert_management.configuration.dir_configuration import DirConfiguration
from cert_management.contract.store_provider_contract import (
    StoreProviderContract,
)
from cert_management.openssl_library.cryptography.private_key import PrivateKey


class CreatePrivateKey:
    def __init__(self, store_service: StoreProviderContract, passphrase=None):
        DirConfiguration().create_dirs()
        self._dirs = DirConfiguration().get_dir()
        self._private_key = None
        self._public_key = None
        self._passphrase = passphrase
        self._private_key_module = PrivateKey()
        self._store_service = store_service

    async def execute(self, save=False, is_ca_private_key=False) -> RSAPrivateKey:
        self._private_key, self._public_key = (
            self._private_key_module.create_private_key(self._passphrase)
        )
        if save:
            await self.save(is_ca_private_key=is_ca_private_key)
        return self._private_key

    async def save(self, is_ca_private_key=False):
        private_key_bytes, public_key_bytes = self._private_key_module.convert_to_file(
            self._private_key, self._public_key, self._passphrase
        )
        data = [
            {
                "id": "privatekey",
                "title": "chave privada",
                "field_type": "Concealed",
                "section_id": "batatinha",
                "value": private_key_bytes.decode("utf-8"),
            },
            {
                "id": "publickey",
                "title": "chave pública",
                "field_type": "Text",
                "section_id": "batatinha",
                "value": public_key_bytes.decode("utf-8"),
            },
        ]
        if self._passphrase is not None:
            data.append(
                {
                    "id": "passphase",
                    "title": "password",
                    "field_type": "Concealed",
                    "section_id": "batatinha",
                    "value": self._passphrase,
                }
            )
        title = "certificate"
        if is_ca_private_key:
            title = "private key CA"
        await self._store_service.store_many(data, {"title": title})
