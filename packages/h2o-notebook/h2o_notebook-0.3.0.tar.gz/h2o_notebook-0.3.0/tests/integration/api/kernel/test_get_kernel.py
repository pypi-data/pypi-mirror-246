import http
import os

import pytest

from h2o_notebook.clients.kernel.client import KernelClient
from h2o_notebook.clients.kernel.type import KernelType
from h2o_notebook.exception import CustomApiException


def test_get_kernel(kernel_client_super_admin: KernelClient, kernels_cleanup_after):
    yaml_spec = open(os.path.join(os.path.dirname(__file__), "pod_template_spec.yaml"),"r").read()

    kernel_client_super_admin.create_kernel(
        kernel_id="my-first-kernel",
        kernel_type=KernelType.TYPE_R,
        image="something",
        display_name="my first kernel",
        cpu_request=1,
        cpu_limit=2,
        gpu_resource_name="gpu-resource-name",
        gpu_request=3,
        gpu_limit=4,
        memory_bytes_request="5",
        memory_bytes_limit="6",
        yaml_pod_template_spec=yaml_spec,
    )

    k = kernel_client_super_admin.get_kernel(kernel_id="my-first-kernel")

    assert k.name == "kernels/my-first-kernel"
    assert k.kernel_id == "my-first-kernel"
    assert k.type == KernelType.TYPE_R
    assert k.display_name == "my first kernel"
    assert k.image == "something"
    assert k.cpu_request == 1
    assert k.cpu_limit == 2
    assert k.gpu_resource_name == "gpu-resource-name"
    assert k.gpu_request == 3
    assert k.gpu_limit == 4
    assert k.memory_bytes_request == "5"
    assert k.memory_bytes_limit == "6"
    assert k.yaml_pod_template_spec == yaml_spec
    assert k.create_time is not None
    assert k.creator is not None
    assert k.update_time is None
    assert k.updater is None

def test_get_kernel_not_found(kernel_client_super_admin: KernelClient, kernels_cleanup_after):
    with pytest.raises(CustomApiException) as exc:
        # Try to create Kernel with the same ID.
        kernel_client_super_admin.get_kernel(
            kernel_id="my-first-kernel",
        )

    assert exc.value.status == http.HTTPStatus.NOT_FOUND
