import typer
from typer import Context, Exit, Option

from cert_management import __version__
from cert_management.cli import certificate_authority_cli, certificate_cli
from cert_management.cli.style import print_main_help

app = typer.Typer()


def version_func(flag):
    if flag:
        print(__version__)
        raise Exit(code=0)


def create_cli_app() -> typer.Typer:
    app.add_typer(certificate_authority_cli.app, name="certificate-authority")
    app.add_typer(certificate_cli.app, name="certificate")
    return app


@app.callback(invoke_without_command=True)
def main(
    ctx: Context,
    version: bool = Option(False, callback=version_func, is_flag=True),
):

    if ctx.invoked_subcommand:
        return
    print_main_help()
