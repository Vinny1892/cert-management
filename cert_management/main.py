import typer

from cert_management.cli.main import create_cli_app

app: typer.Typer = create_cli_app()
app()
