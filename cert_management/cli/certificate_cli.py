import asyncio
from functools import wraps

from typer import Typer, Argument
from rich import print

from cert_management.commands.create_private_key_command import CreatePrivateKey
from cert_management.store.one_password_store_service import OnePasswordStoreService

app = Typer()

def typer_async(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper

@app.command()
@typer_async
async def sign_certificate(
        path: str = Argument('', help="Path to the certificate file"),
):
    print("Signing certificate")
    one_password =  await OnePasswordStoreService.build()
    await  CreatePrivateKey(store_service=one_password, passphrase='').execute(save=True)
