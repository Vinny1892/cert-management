from typer import Argument, Typer

from cert_management.cli import typer_async
from cert_management.cli.style import print_error
from cert_management.commands.create_private_key_command import (
    CreatePrivateKey,
)
from cert_management.store_provider.provider import choose_provider

app = Typer()


@app.command()
@typer_async
async def create(
    password: str = Argument(None, help="Password for private key"),
):
    try:
        provider = choose_provider()
        await CreatePrivateKey(store_service=provider, passphrase=password).execute(
            save=True
        )
    except Exception as exception:
        print_error(exception)
