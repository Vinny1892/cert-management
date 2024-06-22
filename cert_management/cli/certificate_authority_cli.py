import asyncio
import os
from functools import wraps

from typer import Option, Typer

from cert_management.cli import typer_async
from cert_management.cli.style import print_error
from cert_management.store.one_password_store_service import (
    OnePasswordStoreService,
)
from cert_management.use_case.create_certificate_authority_use_case import (
    CreateCertificateAuthorityUseCase,
    OptionsCreateCertificateAuthority,
)

app = Typer()


@app.command()
@typer_async
async def create(
    path_private_key: str = Option(None, help="Path to the private key file"),
    password_private_key: str = Option(
        None, help="Password for private key", envvar="PASSWORD_PRIVATE_KEY"
    )
):
    try:
        options = OptionsCreateCertificateAuthority(
            path_private_key=path_private_key, password_private_key=password_private_key
        )
        one_password = await OnePasswordStoreService.build()
        await CreateCertificateAuthorityUseCase(
            store_service=one_password, options=options
        ).handle()
    except Exception as e:
        print_error(str(e))
        os.exit(1)
