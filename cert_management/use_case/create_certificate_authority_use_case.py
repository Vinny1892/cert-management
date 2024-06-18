from cert_management.commands.create_ca_command import CreateCertificateAuthorityCommand
from cert_management.commands.create_private_key_command import CreatePrivateKey
from cert_management.contract.store_service_contract import StoreServiceContract

import random
import string

class CreateCertificateAuthorityUseCase:

    def __init__(self, store_service: StoreServiceContract):
        self.store = store_service

    async def handle(self):
        password = self._generate_password()
        pk = await CreatePrivateKey(store_service=self.store, passphrase=password).execute(save=True)
        await CreateCertificateAuthorityCommand(store_service=self.store, private_key=pk).execute(save=True)
        


    def _generate_password(self,length=12, use_uppercase=True, use_lowercase=True, use_numbers=True, use_symbols=True):
        characters = ''
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

        password = ''.join(random.choice(characters) for _ in range(length))
        return password

