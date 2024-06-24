from unittest.mock import patch, AsyncMock, create_autospec
import os

from typer.testing import CliRunner

from cert_management.cli.main import create_cli_app
from cert_management.contract.store_provider_contract import StoreProviderContract

runner = CliRunner()
app = create_cli_app()

@patch('cert_management.cli.certificate_authority_cli.CreateCertificateAuthorityUseCase')
@patch('cert_management.cli.certificate_authority_cli.choose_provider')
def test_create_certificate_authority_cli_error_in_use_case(
    mock_chose_provider,
    mock_create_certificate_authority_use_case
):
    error = "deu erro no comando"
    mock_create_certificate_authority_use_case.return_value.handle = AsyncMock(side_effect=Exception(error))
    mock_store_provider = create_autospec(StoreProviderContract, instance=True)
    mock_chose_provider.return_value = mock_store_provider
    result = runner.invoke(app, ["certificate-authority", "create" ,"--path-private-key=teste"])
    assert  error in result.stdout
    assert result.exit_code == 1



@patch('cert_management.cli.certificate_authority_cli.CreateCertificateAuthorityUseCase')
@patch('cert_management.cli.certificate_authority_cli.choose_provider')
def test_create_certificate_authority_cli_error_in_provider_store(
        mock_chose_provider,
        mock_create_certificate_authority_use_case
):
    error = "deu erro no comando"

    mock_chose_provider.side_effect = Exception(error)
    mock_create_certificate_authority_use_case.return_value.handle = AsyncMock(side_effect=Exception(error))

    result = runner.invoke(app, ["certificate-authority", "create" ,"--path-private-key=teste"])
    assert  error in result.stdout
    assert result.exit_code == 1
    mock_create_certificate_authority_use_case.handle.assert_not_called()

@patch('cert_management.cli.certificate_authority_cli.CreateCertificateAuthorityUseCase')
@patch('cert_management.cli.certificate_authority_cli.choose_provider')
def test_create_certificate_authority_with_load_private_key(
        mock_chose_provider,
        mock_create_certificate_authority_use_case
):
    success_message = "Certificate authority created successfully"
    mock_create_certificate_authority_use_case.return_value.handle = AsyncMock(return_value=None)
    mock_chose_provider.return_value = create_autospec(StoreProviderContract, instance=True)
    result = runner.invoke(app, ["certificate-authority", "create" ,"--path-private-key=teste"])
    assert result.exit_code == 0
    assert success_message in result.stdout


@patch('cert_management.cli.certificate_authority_cli.CreateCertificateAuthorityUseCase')
@patch('cert_management.cli.certificate_authority_cli.choose_provider')
def test_create_certificate_authority_without_load_private_key(
        mock_chose_provider,
        mock_create_certificate_authority_use_case
):
    success_message = "Certificate authority created successfully"
    mock_create_certificate_authority_use_case.return_value.handle = AsyncMock(return_value=None)
    mock_chose_provider.return_value = create_autospec(StoreProviderContract, instance=True)
    result = runner.invoke(app, ["certificate-authority", "create"])
    assert result.exit_code == 0
    assert success_message in result.stdout