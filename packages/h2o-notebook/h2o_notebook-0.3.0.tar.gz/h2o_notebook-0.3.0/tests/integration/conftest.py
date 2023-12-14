import os

import h2o_authn
import pytest as pytest
from h2o_authn import TokenProvider

import h2o_notebook
from h2o_notebook.clients.kernel.client import KernelClient


@pytest.fixture(scope="session")
def session():
    return h2o_notebook.Session()

@pytest.fixture(scope="session")
def token_provider_user() -> TokenProvider:
    return h2o_authn.TokenProvider(
        refresh_token=os.getenv("PLATFORM_TOKEN_USER"),
        issuer_url=os.getenv("PLATFORM_OIDC_URL"),
        client_id=os.getenv("PLATFORM_OIDC_CLIENT_ID"),
    )

@pytest.fixture(scope="session")
def token_provider_super_admin() -> TokenProvider:
    return h2o_authn.TokenProvider(
        refresh_token=os.getenv("PLATFORM_TOKEN_SUPER_ADMIN"),
        issuer_url=os.getenv("PLATFORM_OIDC_URL"),
        client_id=os.getenv("PLATFORM_OIDC_CLIENT_ID"),
    )

@pytest.fixture(scope="session")
def kernel_client_user(token_provider_user: TokenProvider):
    return KernelClient(
        server_url=os.getenv("NOTEBOOK_SERVER_URL"),
        token_provider=token_provider_user,
        verify_ssl=False,
    )

@pytest.fixture(scope="session")
def kernel_client_super_admin(token_provider_super_admin: TokenProvider):
    return KernelClient(
        server_url=os.getenv("NOTEBOOK_SERVER_URL"),
        token_provider=token_provider_super_admin,
        verify_ssl=False,
    )

@pytest.fixture(scope="function")
def kernels_cleanup_after(kernel_client_super_admin: KernelClient):
    yield

    kernels = kernel_client_super_admin.list_all_kernels()
    for k in kernels:
        kernel_client_super_admin.delete_kernel(kernel_id=k.kernel_id)