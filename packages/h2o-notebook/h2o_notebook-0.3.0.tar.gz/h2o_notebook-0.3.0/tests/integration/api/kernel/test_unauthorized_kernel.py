import http
import os

import pytest

from h2o_notebook.clients.kernel.client import KernelClient
from h2o_notebook.clients.kernel.type import KernelType
from h2o_notebook.exception import CustomApiException


def test_create_unauthorized(kernel_client_user: KernelClient, kernels_cleanup_after):
    with pytest.raises(CustomApiException) as exc:
        kernel_client_user.create_kernel(
            kernel_id="my-first-kernel",
            kernel_type=KernelType.TYPE_PYTHON,
            image="something",
        )
    assert exc.value.status == http.HTTPStatus.FORBIDDEN

@pytest.mark.skip(reason="auth disabled for now")
def test_get_unauthorized(
        kernel_client_super_admin: KernelClient,
        kernel_client_user: KernelClient,
        kernels_cleanup_after,
):
    k = kernel_client_super_admin.create_kernel(
        kernel_id="my-first-kernel",
        kernel_type=KernelType.TYPE_PYTHON,
        image="something",
    )

    kernel_client_user.get_kernel(kernel_id=k.kernel_id)
    # TODO enable test
    # with pytest.raises(CustomApiException) as exc:
    #     kernel_client_user.get_kernel(kernel_id=k.kernel_id)
    # assert exc.value.status == http.HTTPStatus.FORBIDDEN


def test_list_unauthorized(kernel_client_user: KernelClient, kernels_cleanup_after):
    kernel_client_user.list_kernels()
    # # TODO enable test
    # with pytest.raises(CustomApiException) as exc:
    #     kernel_client_user.list_kernels()
    # assert exc.value.status == http.HTTPStatus.FORBIDDEN

def test_update_unauthorized(
        kernel_client_super_admin: KernelClient,
        kernel_client_user: KernelClient,
        kernels_cleanup_after,
):
    k = kernel_client_super_admin.create_kernel(
        kernel_id="my-first-kernel",
        kernel_type=KernelType.TYPE_PYTHON,
        image="something",
    )

    with pytest.raises(CustomApiException) as exc:
        kernel_client_user.update_kernel(kernel=k)
    assert exc.value.status == http.HTTPStatus.FORBIDDEN

def test_delete_unauthorized(
        kernel_client_super_admin: KernelClient,
        kernel_client_user: KernelClient,
        kernels_cleanup_after,
):
    k = kernel_client_super_admin.create_kernel(
        kernel_id="my-first-kernel",
        kernel_type=KernelType.TYPE_PYTHON,
        image="something",
    )

    with pytest.raises(CustomApiException) as exc:
        kernel_client_user.delete_kernel(kernel_id=k.kernel_id)
    assert exc.value.status == http.HTTPStatus.FORBIDDEN
