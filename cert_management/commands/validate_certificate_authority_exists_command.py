from cert_management.contract.store_provider_contract import (
    StoreProviderContract,
)


class ValidateCertificateAuthorityExistsCommand:

    def __init__(self, store_service: StoreProviderContract) -> None:
        self.store_service = store_service

    def execute(self) -> bool:
        return self.store_service.item_exists()
