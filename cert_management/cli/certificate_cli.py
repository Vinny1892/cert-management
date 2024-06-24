import asyncio
from functools import wraps

from rich import print
from typer import Argument, Typer

from cert_management.cli import typer_async
from cert_management.cli.style import print_error
from cert_management.commands.create_private_key_command import (
    CreatePrivateKey,
)
# from cert_management.store_provider.one_password_store_provider import (
#     OnePasswordStoreService,
# )

app = Typer()


@app.command()
@typer_async
async def sign_certificate(
    path: str = Argument("", help="Path to the certificate file"),
):
    try:
        print("sign certificate")
        # one_password = await OnePasswordStoreService.build()
        # await CreatePrivateKey(store_service=one_password, passphrase="").execute(
        #     save=True
        # )
    except Exception as exception:
        print_error(exception)
