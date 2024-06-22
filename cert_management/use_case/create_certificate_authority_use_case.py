import random
import string
from dataclasses import dataclass

from cert_management.commands.create_ca_command import (
    CreateCertificateAuthorityCommand,
)
from cert_management.commands.create_private_key_command import (
    CreatePrivateKey,
)
from cert_management.contract.store_service_contract import (
    StoreServiceContract,
)
from cert_management.openssl_library.cryptography.private_key import PrivateKey


@dataclass
class OptionsCreateCertificateAuthority:
    """
    class to register options in which by CreateCertificateAuthorityUseCase
    """

    path_private_key: str | None
    password_private_key: str | None


class CreateCertificateAuthorityUseCase:
    """
     Create certificate authority use case, this class is responsible for all flow to create a valid certificate authority

    Args:
       store_service: provider to use for store files generated in this use case
       options: options for change default behavior for this use case, list of options
       [ path_private_key, password_private_key ]

    Attributes:
       store: provider to use for store files generated in this use case
       options: options for change default behavior for this use case, list of options
       [ path_private_key, password_private_key ]

    """

    def __init__(
        self,
        store_service: StoreServiceContract,
        options: OptionsCreateCertificateAuthority,
    ) -> None:
        self.store = store_service
        self.options = options

    async def handle(self):
        if self.options.path_private_key is None:
            await self._create_certificate_authority_without_load_private_key()
        else:
            await self._create_certificate_authority_with_load_private_key()

    async def _create_certificate_authority_with_load_private_key(self):
        private_key_module = PrivateKey()
        file = await self.store.get_item(self.options.path_private_key)
        pk = private_key_module.load_pk(
            file=file, password=self.options.password_private_key
        )
        return await CreateCertificateAuthorityCommand(
            store_service=self.store, private_key=pk
        ).execute(save=True)

    async def _create_certificate_authority_without_load_private_key(self) -> None:
        password = self._generate_password()
        pk = await CreatePrivateKey(
            store_service=self.store, passphrase=password
        ).execute(save=True, is_ca_private_key=True)
        return await CreateCertificateAuthorityCommand(
            store_service=self.store, private_key=pk
        ).execute(save=True)

    def _generate_password(
        self,
        length=12,
        use_uppercase=True,
        use_numbers=True,
        use_symbols=True,
    ) -> str:
        characters = string.ascii_lowercase

        if use_uppercase:
            characters += string.ascii_uppercase
        if use_numbers:
            characters += string.digits
        if use_symbols:
            characters += string.punctuation

        password = "".join(random.choice(characters) for _ in range(length))
        return password
