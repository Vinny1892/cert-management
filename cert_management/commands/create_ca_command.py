from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

from cert_management.configuration.dir_configuration import DirConfiguration
from cert_management.contract.store_provider_contract import (
    StoreProviderContract,
)
from cert_management.openssl_library.cryptography.CertificateAuthority import (
    CertificateAuthority,
)


class CreateCertificateAuthorityCommand:
    def __init__(self, store_service: StoreProviderContract, private_key: RSAPrivateKey):
        DirConfiguration().create_dirs()
        self._dirs = DirConfiguration().get_dir()
        self._private_key = private_key
        self._cert = None
        self._encoding = None
        self._certificate_authority = True
        self._certificate_authority_command = CertificateAuthority()
        self._store_service = store_service

    async def execute(self, save=False) -> None:
        if self._certificate_authority:
            self._cert, self._encoding = self._certificate_authority_command.create(
                self._private_key
            )
        if save:
            await self.save()

    async def save(self):
        file = self._certificate_authority_command.convert_to_file()
        await self._store_service.store(
            file,
            "certificate authority",
            {
                "field_type": "Text",
                "title": "certificate authority",
                "category": "SecureNote",
            },
        )
