import os

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from onepassword.types import ItemField

from cert_management.configuration.dir_configuration import DirConfiguration
from cert_management.contract.store_service_contract import StoreServiceContract
from cert_management.openssl_library.cryptograph.PrivateKey import PrivateKey
from datetime import datetime

class CreatePrivateKey:
    def __init__(self, store_service: StoreServiceContract ,passphrase: str):
        DirConfiguration().create_dirs()
        self._dirs = DirConfiguration().get_dir()
        self._private_key = None
        self._public_key = None
        self._passphrase = passphrase
        self._private_key_module = PrivateKey()
        self._store_service = store_service

    async def execute(self, save=False, ca_private_key=False) -> RSAPrivateKey:
        self._private_key, self._public_key =  self._private_key_module.create_private_key(self._passphrase)
        private_key_name ='ca_private_key' if ca_private_key else f'private_key_{datetime.now().strftime("%Y%m%d%H%M%S")}'
        if save:
            await self.save(os.path.join(self._dirs["private"],private_key_name))
        return self._private_key

    async def save(self, path: str):
        private_key_bytes, public_key_bytes = self._private_key_module.convert_to_file(self._private_key, self._public_key ,self._passphrase)
        data = [
            {
                "id": "privatekey",
                "title": "chave privada",
                "field_type": "Concealed",
                "section_id": "batatinha",
                "value": private_key_bytes.decode('utf-8')
            },
            {
                "id": "publickey",
                "title": "chave pública",
                "field_type": "Text",
                "section_id": "batatinha",
                "value": public_key_bytes.decode('utf-8')
            }
        ]
        await self._store_service.store_many(data)

       # with open(path, "wb") as f:
       #     f.write(key_bytes)