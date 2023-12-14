import pprint

from h2o_notebook.clients.kernel.type import KernelType
from h2o_notebook.clients.kernel.type import (
    from_api_object as from_kernel_type_api_object,
)
from h2o_notebook.gen.model.kernel_resource import KernelResource
from h2o_notebook.gen.model.v1_kernel import V1Kernel


class Kernel:
    """Kernel object."""

    def __init__(
            self,
            name: str,
            display_name: str,
            type: KernelType,
            image: str,
            cpu_request: int,
            cpu_limit: int,
            gpu_resource_name: str,
            gpu_request: int,
            gpu_limit: int,
            memory_bytes_request: int,
            memory_bytes_limit: int,
            yaml_pod_template_spec: str,
            create_time: str,
            creator: str,
            update_time: str,
            updater: str,
    ):
        self.name = name
        self.display_name = display_name
        self.type = type
        self.image = image
        self.cpu_request = cpu_request
        self.cpu_limit = cpu_limit
        self.gpu_resource_name = gpu_resource_name
        self.gpu_request = gpu_request
        self.gpu_limit = gpu_limit
        self.memory_bytes_request = memory_bytes_request
        self.memory_bytes_limit = memory_bytes_limit
        self.yaml_pod_template_spec = yaml_pod_template_spec
        self.create_time = create_time
        self.creator = creator
        self.update_time = update_time
        self.updater = updater

        if name:
            self.kernel_id = self.name.split("/")[1]

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)


    def to_api_object(self) -> KernelResource:
        return KernelResource(
            display_name = self.display_name,
            type = self.type.to_api_object(),
            image = self.image,
            cpu_request = self.cpu_request,
            cpu_limit = self.cpu_limit,
            gpu_resource_name = self.gpu_resource_name,
            gpu_request = self.gpu_request,
            gpu_limit = self.gpu_limit,
            memory_bytes_request = self.memory_bytes_request,
            memory_bytes_limit = self.memory_bytes_limit,
            yaml_pod_template_spec = self.yaml_pod_template_spec,
        )


def from_api_object(api_object: V1Kernel) -> Kernel:
    return Kernel(
        name = api_object.name,
        display_name = api_object.display_name,
        type = from_kernel_type_api_object(api_object.type),
        image = api_object.image,
        cpu_request = api_object.cpu_request,
        cpu_limit = api_object.cpu_limit,
        gpu_resource_name = api_object.gpu_resource_name,
        gpu_request = api_object.gpu_request,
        gpu_limit = api_object.gpu_limit,
        memory_bytes_request = api_object.memory_bytes_request,
        memory_bytes_limit = api_object.memory_bytes_limit,
        yaml_pod_template_spec = api_object.yaml_pod_template_spec,
        create_time = api_object.create_time,
        creator = api_object.creator,
        update_time = api_object.update_time,
        updater = api_object.updater,
    )