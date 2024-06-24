from cert_management.contract.store_provider_contract import StoreProviderContract

class FilesystemStoreProvider(StoreProviderContract):
    @classmethod
    def build(cls):
        pass

    def store(self, item, name, config: dict):
        pass

    def store_many(self, data, config):
        pass

    def get_item(self, path):
        pass

    def item_exists(self):
        pass