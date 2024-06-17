from cert_management.contract.store_service_contract import StoreServiceContract


class ValidateCertificateAuthorityExistsCommand:

    def __init__(self, store_service: StoreServiceContract) -> None:
        self.store_service = store_service

    def execute(self) -> bool:
        return self.store_service.item_exists()



