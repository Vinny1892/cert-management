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
from cert_management.openssl_library.cryptograph.PrivateKey import PrivateKey


@dataclass
class OptionsCreateCertificateAuthority:
    """
    class to register options in which by CreateCertificateAuthorityUseCase
    """

    path_private_key: str
    password_private_key: str


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
        private_key_module = PrivateKey()
        if self.options.path_private_key is None:
            password = self._generate_password()
            pk = await CreatePrivateKey(
                store_service=self.store, passphrase=password
            ).execute(save=True, is_ca_private_key=True)
        else:
            # TODO: handle exception if certificate has encrypted and password is not provided
            file = await self.store.get_item(self.options.path_private_key)
            pk = private_key_module.load_pk(
                file=file, password=self.options.password_private_key
            )
        await CreateCertificateAuthorityCommand(
            store_service=self.store, private_key=pk
        ).execute(save=True)

    def _generate_password(
        self,
        length=12,
        use_uppercase=True,
        use_lowercase=True,
        use_numbers=True,
        use_symbols=True,
    ):
        characters = ""
        if use_uppercase:
            characters += string.ascii_uppercase
        if use_lowercase:
            characters += string.ascii_lowercase
        if use_numbers:
            characters += string.digits
        if use_symbols:
            characters += string.punctuation

        if not characters:
            raise ValueError("At least one type of character must be selected")

        password = "".join(random.choice(characters) for _ in range(length))
        return password
