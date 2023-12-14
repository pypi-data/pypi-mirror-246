from enum import Enum

from h2o_notebook.gen.model.v1_kernel_type import V1KernelType


class KernelType(Enum):
    TYPE_UNSPECIFIED = "TYPE_UNSPECIFIED"
    TYPE_PYTHON = "TYPE_PYTHON"
    TYPE_R = "TYPE_R"
    TYPE_SPARK_PYTHON = "TYPE_SPARK_PYTHON"
    TYPE_SPARK_R = "TYPE_SPARK_R"

    def to_api_object(self) -> V1KernelType:
        return V1KernelType(self.name)


def from_api_object(kernel_type: V1KernelType) -> KernelType:
    return KernelType(str(kernel_type))
