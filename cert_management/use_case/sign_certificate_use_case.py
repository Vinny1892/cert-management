from cert_management.commands.create_private_key_command import (
    CreatePrivateKey,
)
from cert_management.commands.validate_certificate_authority_exists_command import (
    ValidateCertificateAuthorityExistsCommand,
)
from cert_management.contract.store_provider_contract import (
    StoreProviderContract,
)


class SignCertificateUseCase:

    def __init__(self, store_service: StoreProviderContract):
        self.store = store_service

    def handle(self):
        ValidateCertificateAuthorityExistsCommand(store_service=self.store).execute()
        CreatePrivateKey(store_service=self.store).execute(save=True)
        ## sign_certificate
