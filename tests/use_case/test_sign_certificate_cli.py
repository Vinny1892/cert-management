from typer.testing import CliRunner

from cert_management.cli.main import create_cli_app

runner = CliRunner()
app = create_cli_app()


def test_sign_certificate_cli():
    result = runner.invoke(app, ["certificate-authority", "create"])
    print("AQUI")
    print(result.stdout)
    assert result.exit_code == 0
