import typer

from cert_management.cli import certificate_authority_cli, certificate_cli


def create_cli_app() -> typer.Typer:
    app = typer.Typer()
    app.add_typer(certificate_authority_cli.app, name="certificate-authority")
    app.add_typer(certificate_cli.app, name="certificate")
    return app