import os

from onepassword.client import Client
from onepassword.types import Item, ItemField, ItemSection

from cert_management.configuration.variables import config
from cert_management.contract.store_service_contract import (
    StoreServiceContract,
)


class OnePasswordStoreService(StoreServiceContract):

    def item_exists(self):
        pass

    def __init__(self, client_one_password) -> None:
        self._client_one_password = client_one_password

    @classmethod
    async def build(cls) -> "OnePasswordStoreService":
        token = config("ONE_PASSWORD_TOKEN")
        client = await Client.authenticate(
            auth=token,
            integration_name="one_password_token",
            integration_version="v1.0.0",
        )
        instance = cls(client)
        return instance

    async def store_many(self, items, config_item) -> None:
        vault_id = "ezkhx3p2zkaekyr47u3cjdlkoe"
        data = list(
            map(
                lambda item: ItemField(
                    id=item["id"],
                    title=item["title"],
                    field_type=item["field_type"],
                    section_id="batatinha",
                    value=item["value"],
                ),
                items,
            )
        )
        to_create = Item(
            id="",
            title=config_item["title"],
            category="SshKey",
            vault_id="ezkhx3p2zkaekyr47u3cjdlkoe",
            fields=data,
            sections=[ItemSection(id="batatinha", title="")],
        )
        await self._client_one_password.items.create(to_create)

    async def store(self, value_field, field_name, config_field) -> None:
        # SshKey, SecureNote
        to_create = Item(
            id="",
            title=config_field["title"],
            category=config_field["category"],
            vault_id="ezkhx3p2zkaekyr47u3cjdlkoe",
            fields=[
                ItemField(
                    id=field_name,
                    title=field_name,
                    field_type=config_field["field_type"],
                    section_id="batatinha",
                    value=value_field,
                ),
            ],
            sections=[ItemSection(id="batatinha", title="")],
        )

        await self._client_one_password.items.create(to_create)

    async def _setup_one_password_client(self) -> None:
        token = os.getenv("OP_SERVICE_ACCOUNT_TOKEN")
        self.client = await Client.authenticate(
            auth=token, integration_name="teste", integration_version="v1.0.0"
        )

    async def get_item(self, path) -> str:
        """
         method get item in 1password
        :param path: path where item is stored in format op://vault/item_name/field
        :return: value of item search for example (private key, certificate, password, text)
        """

        value = await self._client_one_password.secrets.resolve(path)
        return value
