from unittest.mock import create_autospec, AsyncMock

from cert_management.contract.store_service_contract import StoreServiceContract
from cert_management.use_case.create_certificate_authority_use_case import CreateCertificateAuthorityUseCase

async def test_create_certificate_authority():
    mock_store_service = create_autospec(StoreServiceContract, instance=True)
    mock_store_service.store = AsyncMock(return_value=None)

    await CreateCertificateAuthorityUseCase(mock_store_service).handle()
    mock_store_service.store.assert_awaited_once()