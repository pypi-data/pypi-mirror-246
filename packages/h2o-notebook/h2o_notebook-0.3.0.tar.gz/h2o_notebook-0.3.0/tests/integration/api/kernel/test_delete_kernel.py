import http
import os

import pytest

from h2o_notebook.clients.kernel.client import KernelClient
from h2o_notebook.clients.kernel.type import KernelType
from h2o_notebook.exception import CustomApiException


def test_delete_kernel(kernel_client_super_admin: KernelClient, kernels_cleanup_after):
    k = kernel_client_super_admin.create_kernel(
        kernel_id="my-first-kernel",
        kernel_type=KernelType.TYPE_PYTHON,
        image="something",
    )

    kernel_client_super_admin.delete_kernel(kernel_id=k.kernel_id)

    with pytest.raises(CustomApiException) as exc:
        kernel_client_super_admin.get_kernel(kernel_id=k.kernel_id)
    assert exc.value.status == http.HTTPStatus.NOT_FOUND

def test_delete_kernel_not_found(kernel_client_super_admin: KernelClient, kernels_cleanup_after):
    with pytest.raises(CustomApiException) as exc:
        kernel_client_super_admin.delete_kernel(kernel_id="not-found")
    assert exc.value.status == http.HTTPStatus.NOT_FOUND