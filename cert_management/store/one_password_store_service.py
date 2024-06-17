import os

from onepassword.types import Item, ItemField, ItemSection

from cert_management.contract.store_service_contract import StoreServiceContract
from onepassword.client import Client
from cert_management.configuration.variables import config


class OnePasswordStoreService(StoreServiceContract):

    def item_exists(self):
        pass

    def __init__(self, client_one_password):
        self._client_one_password = client_one_password


    @classmethod
    async def build(cls):
        token = config("ONE_PASSWORD_TOKEN")
        client = await Client.authenticate(auth=token, integration_name="one_password_token", integration_version="v1.0.0")
        instance = cls(client)
        return instance

    async def store_many(self, items):
        vault_id = 'ezkhx3p2zkaekyr47u3cjdlkoe'
        data = list(map(lambda item: ItemField(id=item['id'], title= item['title'], field_type=item['field_type'],
                    section_id='batatinha',
                    value=item['value']), items))
        to_create = Item(
            id="",
            title="test_app",
            category="SshKey",
            vault_id="ezkhx3p2zkaekyr47u3cjdlkoe",
            fields=data,
            sections=[ItemSection(id="batatinha", title="")],
        )
        await self._client_one_password.items.create(to_create)


    async def store(self, item, field_name, config_field):
        to_create = Item(
            id="",
            title="test_app",
            category="SshKey",
            vault_id="ezkhx3p2zkaekyr47u3cjdlkoe",
            fields=[
                ItemField(
                    id="privatekey",
                    title=field_name,
                    field_type=config_field['field_type'],
                    section_id='batatinha',
                    value=item,
                ),

            ],
            sections=[ItemSection(id="batatinha", title="")],
        )

        await self._client_one_password.items.create(to_create)

    async def _setup_one_password_client(self):
        token = os.getenv("OP_SERVICE_ACCOUNT_TOKEN")
        print(token)
        self.client = await Client.authenticate(auth=token, integration_name="teste",  integration_version="v1.0.0")

    async def get_item(self):
        value = await self._client_one_password.secrets.resolve("op://CA/Chave Privada root CA/private_key")
        print(value)