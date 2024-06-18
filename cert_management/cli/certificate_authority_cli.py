from cert_management.commands.create_ca_command import CreateCertificateAuthorityCommand
from cert_management.commands.create_private_key_command import CreatePrivateKey
from cert_management.store.one_password_store_service import OnePasswordStoreService
from cert_management.use_case.create_certificate_authority_use_case import CreateCertificateAuthorityUseCase
from typer import Typer, Argument
import asyncio
from functools import wraps
app = Typer()

def typer_async(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper

@app.command()
@typer_async
async def create(
        path: str = Argument('', help="Path to the certificate file"),
):
    print("create ca")
    one_password =  await OnePasswordStoreService.build()
    await  CreateCertificateAuthorityUseCase(store_service=one_password).handle()