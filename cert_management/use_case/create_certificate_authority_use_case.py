from cert_management.commands.CreateCACommand import CreateCertificateAuthorityCommand
from cert_management.commands.CreatePrivateKey import CreatePrivateKey
from cert_management.contract.store_service_contract import StoreServiceContract


class CreateCertificateAuthorityUseCase:

    def __init__(self, store_service: StoreServiceContract):
        self.store = store_service

    async def handle(self):
        pk = await CreatePrivateKey(store_service=self.store, passphrase='').execute(save=True)
        CreateCertificateAuthorityCommand(store_service=self.store, private_key=pk).execute(save=True)



