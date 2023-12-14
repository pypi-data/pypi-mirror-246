import http
import os

import pytest

from h2o_notebook.clients.kernel.client import KernelClient
from h2o_notebook.clients.kernel.type import KernelType
from h2o_notebook.exception import CustomApiException


@pytest.mark.parametrize(
    ["page_size", "page_token"],
    [
        (-20, ""),
        (0, "non-existing-token"),
    ],
)
def test_list_validation(
        kernel_client_super_admin: KernelClient, page_size, page_token
):
    with pytest.raises(CustomApiException) as exc:
        kernel_client_super_admin.list_kernels(
            page_size=page_size,
            page_token=page_token,
        )
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST

def test_list(kernel_client_super_admin: KernelClient, kernels_cleanup_after):
    # Test no profiles found.
    page = kernel_client_super_admin.list_kernels()
    assert len(page.kernels) == 0
    assert page.next_page_token == ""

    # Arrange
    kernel_client_super_admin.create_kernel(
        kernel_id="my-first-kernel",
        kernel_type=KernelType.TYPE_PYTHON,
        image="something",
    )
    kernel_client_super_admin.create_kernel(
        kernel_id="my-second-kernel",
        kernel_type=KernelType.TYPE_PYTHON,
        image="something",
    )
    kernel_client_super_admin.create_kernel(
        kernel_id="my-third-kernel",
        kernel_type=KernelType.TYPE_PYTHON,
        image="something",
    )

    # Test getting first page.
    page = kernel_client_super_admin.list_kernels(page_size=1)
    assert len(page.kernels) == 1
    assert page.next_page_token != ""

    # Test getting second page.
    page = kernel_client_super_admin.list_kernels(
        page_size=1, page_token=page.next_page_token
    )
    assert len(page.kernels) == 1
    assert page.next_page_token != ""

    # Test getting last page.
    page = kernel_client_super_admin.list_kernels(
        page_size=1, page_token=page.next_page_token
    )
    assert len(page.kernels) == 1
    assert page.next_page_token == ""

    # Test exceeding max page size.
    page = kernel_client_super_admin.list_kernels(page_size=1001)
    assert len(page.kernels) == 3
    assert page.next_page_token == ""

def test_list_all(kernel_client_super_admin: KernelClient, kernels_cleanup_after):
    # Arrange
    kernel_client_super_admin.create_kernel(
        kernel_id="my-first-kernel",
        kernel_type=KernelType.TYPE_PYTHON,
        image="something",
    )
    kernel_client_super_admin.create_kernel(
        kernel_id="my-second-kernel",
        kernel_type=KernelType.TYPE_PYTHON,
        image="something",
    )
    kernel_client_super_admin.create_kernel(
        kernel_id="my-third-kernel",
        kernel_type=KernelType.TYPE_PYTHON,
        image="something",
    )

    # Test basic list_all.
    kernels = kernel_client_super_admin.list_all_kernels()
    assert len(kernels) == 3