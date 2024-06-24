from unittest.mock import patch, AsyncMock

from typer.testing import CliRunner

from cert_management.cli.main import create_cli_app

runner = CliRunner()
app = create_cli_app()

@patch('cert_management.store.one_password_store_service.Client', new_callable=AsyncMock)
@patch('cert_management.configuration.variables.Configuration.get')
@patch('cert_management.store.one_password_store_service.OnePasswordStoreService')
@patch('cert_management.use_case.create_certificate_authority_use_case.CreateCertificateAuthorityUseCase.handle', new_callable=AsyncMock)
def test_create_certificate_authority_cli_error_in_use_case(mock_create_certificate_authority_use_case, mock_one_password_storage_service, mock_config,mock_one_password_client):
    error = "deu erro no comando"
    mock_one_password_storage_service.store.return_value = None
    mock_one_password_storage_service.store_many.return_value = None

    mock_one_password_client.authenticate.return_value = AsyncMock(return_value=None)
    mock_config.return_value = "tok3n"
    mock_create_certificate_authority_use_case.side_effect = Exception(error)
    result = runner.invoke(app, ["certificate-authority", "create" ,"--path-private-key=teste"])
    assert  error in result.stdout
    assert result.exit_code == 1
    mock_one_password_storage_service.store.assert_not_called()
    mock_one_password_storage_service.store_many.assert_not_called()


@patch('cert_management.store.one_password_store_service.Client', new_callable=AsyncMock)
@patch('cert_management.configuration.variables.Configuration.get')
@patch('cert_management.store.one_password_store_service.OnePasswordStoreService.build')
@patch('cert_management.use_case.create_certificate_authority_use_case.CreateCertificateAuthorityUseCase.handle', new_callable=AsyncMock)
def test_create_certificate_authority_cli_error_in_provider_store(mock_create_certificate_authority_use_case, mock_one_password_storage_service, mock_config,mock_one_password_client):
    error = "deu erro no comando"
    mock_one_password_storage_service.store.return_value = None
    mock_one_password_storage_service.store_many.return_value = None

    mock_one_password_client.authenticate.return_value = AsyncMock(return_value=None)
    mock_config.return_value = "tok3n"
    mock_one_password_storage_service.side_effect = Exception(error)
    result = runner.invoke(app, ["certificate-authority", "create" ,"--path-private-key=teste"])
    assert  error in result.stdout
    assert result.exit_code == 1
    mock_one_password_storage_service.store.assert_not_called()
    mock_one_password_storage_service.store_many.assert_not_called()
    mock_create_certificate_authority_use_case.assert_not_awaited()