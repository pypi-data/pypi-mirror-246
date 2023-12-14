import http
import os

import pytest

from h2o_notebook.clients.kernel.client import KernelClient
from h2o_notebook.clients.kernel.type import KernelType
from h2o_notebook.exception import CustomApiException


@pytest.mark.parametrize(
    "mask",
    [
        "unknown",
        "invalid character",
        "gpu, *",
        " ",
    ],
)
def test_update_mask_validation(kernel_client_super_admin: KernelClient, mask, kernels_cleanup_after):
    k = kernel_client_super_admin.create_kernel(
        kernel_id="my-first-kernel",
        kernel_type=KernelType.TYPE_PYTHON,
        image="something",
    )

    k.display_name = "Changed Smokerinho"

    with pytest.raises(CustomApiException) as exc:
        kernel_client_super_admin.update_kernel(kernel=k, update_mask=mask)
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST


def test_update(kernel_client_super_admin: KernelClient, kernels_cleanup_after):
    original = kernel_client_super_admin.create_kernel(
        kernel_id="my-first-kernel",
        kernel_type=KernelType.TYPE_PYTHON,
        image="something",
    )

    original.gpu_limit = 1
    original.cpu_request = 2
    original.memory_bytes_request = "3"
    original.storage_bytes_limit = "4"

    # Update profile with update_mask.
    updated = kernel_client_super_admin.update_kernel(original, update_mask="cpu_request,memory_bytes_request")

    assert updated.cpu_request == 2
    assert updated.memory_bytes_request == "3"
    assert updated.gpu_limit == 0

    # Update profile without update_mask.
    updated = kernel_client_super_admin.update_kernel(original)

    assert updated.gpu_limit == 1