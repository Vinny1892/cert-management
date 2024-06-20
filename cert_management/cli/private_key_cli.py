from typer import Argument, Typer

from cert_management.cli import typer_async
from cert_management.cli.style import print_error
from cert_management.commands.create_private_key_command import (
    CreatePrivateKey,
)
from cert_management.store.one_password_store_service import (
    OnePasswordStoreService,
)

app = Typer()


@app.command()
@typer_async
async def create(
    password: str = Argument(None, help="Password for private key"),
):
    try:
        one_password = await OnePasswordStoreService.build()
        await CreatePrivateKey(store_service=one_password, passphrase=password).execute(
            save=True
        )
    except Exception as exception:
        print_error(exception)
