from unittest.mock import AsyncMock, create_autospec, patch

from cert_management.contract.store_service_contract import (
    StoreServiceContract,
)
from cert_management.use_case.create_certificate_authority_use_case import (
    CreateCertificateAuthorityUseCase,
)


@patch("cert_management.configuration.dir_configuration.os")
async def test_create_certificate_authority(mock_os):
    mock_os.makedirs.return_value = None
    mock_store_service = create_autospec(StoreServiceContract, instance=True)
    mock_store_service.store_many = AsyncMock(return_value=None)
    mock_store_service.store = AsyncMock(return_value=None)

    await CreateCertificateAuthorityUseCase(mock_store_service).handle()
    mock_store_service.store_many.assert_awaited_once()
    mock_store_service.store.assert_awaited_once()
