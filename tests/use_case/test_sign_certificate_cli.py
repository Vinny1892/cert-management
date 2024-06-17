from unittest.mock import create_autospec, AsyncMock
from unittest.mock import patch
from cert_management.contract.store_service_contract import StoreServiceContract
from cert_management.use_case.create_certificate_authority_use_case import CreateCertificateAuthorityUseCase
from typer.testing import CliRunner
from cert_management.cli.main import create_cli_app

runner = CliRunner()
app = create_cli_app()

def test_sign_certificate_cli():
    result = runner.invoke(app, ['certificate-authority','create'])
    print("AQUI")
    print(result.stdout )
    assert result.exit_code == 0
