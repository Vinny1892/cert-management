from unittest.mock import AsyncMock, create_autospec, patch

from cert_management.contract.store_provider_contract import (
    StoreProviderContract,
)
from cert_management.openssl_library.cryptography.private_key import PrivateKey
from cert_management.use_case.create_certificate_authority_use_case import (
    CreateCertificateAuthorityUseCase, OptionsCreateCertificateAuthority,
)


@patch("cert_management.configuration.dir_configuration.os")
async def test_create_certificate_authority_with_password_and_create_private_key(mock_os):
    mock_os.makedirs.return_value = None
    mock_store_service = create_autospec(StoreProviderContract, instance=True)
    mock_store_service.store_many = AsyncMock(return_value=None)
    mock_store_service.store = AsyncMock(return_value=None)
    password_private_key = "t3st3!"
    options =  OptionsCreateCertificateAuthority(
            path_private_key=None, password_private_key=password_private_key
        )
    await CreateCertificateAuthorityUseCase(mock_store_service, options=options).handle()
    mock_store_service.store_many.assert_awaited_once()
    mock_store_service.store.assert_awaited_once()

@patch("cert_management.openssl_library.cryptography.private_key.PrivateKey.load_pk")
@patch("cert_management.configuration.dir_configuration.os")
async def test_create_certificate_authority_with_password_and_load_pk(mock_os,mock_load_pk_private_key):
    password_private_key = "t3st3!"
    private_key_string = "private_k3y"
    private_key, _public_key = PrivateKey().create_private_key(passphrase=password_private_key)
    mock_load_pk_private_key.return_value = private_key
    mock_os.makedirs.return_value = None
    mock_store_service = create_autospec(StoreProviderContract, instance=True)
    mock_store_service.get_item = AsyncMock(return_value=private_key_string)
    mock_store_service.store = AsyncMock(return_value=None)
    options =  OptionsCreateCertificateAuthority(
            path_private_key='/mock/path', password_private_key=password_private_key
        )
    await CreateCertificateAuthorityUseCase(mock_store_service, options=options).handle()
    mock_store_service.store.assert_awaited_once()
    mock_store_service.get_item.assert_awaited_once()


@patch("cert_management.openssl_library.cryptography.private_key.PrivateKey.load_pk")
@patch("cert_management.configuration.dir_configuration.os")
async def test_create_certificate_authority_without_password_and_load_pk(mock_os,mock_load_pk_private_key):
    password_private_key = None
    private_key_string = "private_k3y"
    private_key, _public_key = PrivateKey().create_private_key(passphrase=password_private_key)
    mock_load_pk_private_key.return_value = private_key
    mock_os.makedirs.return_value = None
    mock_store_service = create_autospec(StoreProviderContract, instance=True)
    mock_store_service.get_item = AsyncMock(return_value=private_key_string)
    mock_store_service.store = AsyncMock(return_value=None)
    options =  OptionsCreateCertificateAuthority(
            path_private_key='/mock/path', password_private_key=password_private_key
        )
    await CreateCertificateAuthorityUseCase(mock_store_service, options=options).handle()
    mock_store_service.store.assert_awaited_once()
    mock_store_service.get_item.assert_awaited_once()
