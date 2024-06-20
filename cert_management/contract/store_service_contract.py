from abc import ABC, abstractmethod


class StoreServiceContract(ABC):

    @abstractmethod
    def store(self, item, name, config: dict):
        raise Exception("Not implemented method")

    @abstractmethod
    def store_many(self, data, config):
        raise Exception("Not implemented method")

    @abstractmethod
    def get_item(self, path):
        raise Exception("Not implemented method")

    @abstractmethod
    def item_exists(self):
        raise Exception("Not implemented method")
