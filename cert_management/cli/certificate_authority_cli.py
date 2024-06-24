import asyncio
import sys
from functools import wraps

from typer import Option, Typer

from cert_management.cli import typer_async
from cert_management.cli.style import print_error
from cert_management.store_provider.provider import choose_provider

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

        provider = choose_provider()
        await CreateCertificateAuthorityUseCase(
            store_service=provider, options=options
        ).handle()
        print("Certificate authority created successfully")
    except Exception as e:
        print_error(str(e))
        sys.exit(1)
