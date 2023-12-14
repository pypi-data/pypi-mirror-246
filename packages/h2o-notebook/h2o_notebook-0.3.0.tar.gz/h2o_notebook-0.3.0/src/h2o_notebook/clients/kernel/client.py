from typing import Dict
from typing import List
from typing import Optional

from h2o_authn import TokenProvider

from h2o_notebook.clients.auth.token_api_client import TokenApiClient
from h2o_notebook.clients.kernel.kernel import Kernel
from h2o_notebook.clients.kernel.kernel import from_api_object
from h2o_notebook.clients.kernel.page import KernelsPage
from h2o_notebook.clients.kernel.type import KernelType
from h2o_notebook.exception import CustomApiException
from h2o_notebook.gen import ApiException
from h2o_notebook.gen import Configuration
from h2o_notebook.gen.api.kernel_service_api import KernelServiceApi
from h2o_notebook.gen.model.v1_kernel import V1Kernel
from h2o_notebook.gen.model.v1_list_kernels_response import V1ListKernelsResponse


class KernelClient:
    """KernelClient manages Python kernels."""

    def __init__(
            self,
            server_url: str,
            token_provider: TokenProvider,
            verify_ssl: bool = True,
            ssl_ca_cert: Optional[str] = None,
    ):
        configuration = Configuration(host=server_url)
        configuration.verify_ssl = verify_ssl
        configuration.ssl_ca_cert = ssl_ca_cert

        with TokenApiClient(
                configuration, token_provider
        ) as api_client:
            self.api_instance = KernelServiceApi(api_client)

    def create_kernel(
            self,
            kernel_id: str,
            kernel_type: KernelType,
            image: str,
            display_name: str = "",
            cpu_request: int = 0,
            cpu_limit: int = 0,
            gpu_resource_name: str = "",
            gpu_request: int = 0,
            gpu_limit: int = 0,
            memory_bytes_request: str = "0",
            memory_bytes_limit: str = "0",
            yaml_pod_template_spec: str = "",
    ) -> Kernel:
        """Creates a kernel.

        Args:
            kernel_id (str): Kernel ID.
            kernel_type (KernelType): Kernel type.
            image (str): Kernel image.
            display_name (str): Kernel display name.
            cpu_request (int): CPU request.
            cpu_limit (int): CPU limit.
            gpu_resource_name (str): GPU resource name.
            gpu_request (int): GPU request.
            gpu_limit (int): GPU limit.
            memory_bytes_request (str): Memory request.
            memory_bytes_limit (str): Memory limit.
            yaml_pod_template_spec (str): YAML pod template spec.

        Returns:
            Kernel: Kernel object.
        """
        api_object = V1Kernel(
            type=kernel_type.to_api_object(),
            image=image,
            display_name=display_name,
            cpu_request=cpu_request,
            cpu_limit=cpu_limit,
            gpu_resource_name=gpu_resource_name,
            gpu_request=gpu_request,
            gpu_limit=gpu_limit,
            memory_bytes_request=memory_bytes_request,
            memory_bytes_limit=memory_bytes_limit,
            yaml_pod_template_spec=yaml_pod_template_spec,
        )
        created_api_object: V1Kernel

        try:
            created_api_object = self.api_instance.kernel_service_create_kernel(
                kernel_id=kernel_id,
                kernel=api_object,
            ).kernel
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_object(api_object=created_api_object)

    def get_kernel(self, kernel_id: str) -> Kernel:
        """Returns a kernel.

        Args:
            kernel_id (str): Kernel ID.

        Returns:
            Kernel: Kernel object.
        """
        api_object: V1Kernel

        try:
            api_object = self.api_instance.kernel_service_get_kernel(
                name=f"kernels/{kernel_id}",
            ).kernel
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_object(api_object=api_object)

    def list_kernels(
            self,
            page_size: int = 0,
            page_token: str = "",
    ) -> KernelsPage:
        """Lists kernels.

        Args:
            page_size (int): Maximum number of kernels to return in a response.
                If unspecified (or set to 0), at most 50 InternalDAIVersions will be returned.
                The maximum value is 1000; values above 1000 will be coerced to 1000.
            page_token (str): Page token.
                Leave unset to receive the initial page.
                To list any subsequent pages use the value of 'next_page_token' returned from the KernelsPage.

        Returns:
            KernelsPage: KernelsPage object.
        """
        list_response: V1ListKernelsResponse

        try:
            list_response = (
                self.api_instance.kernel_service_list_kernels(
                    page_size=page_size,
                    page_token=page_token,
                )
            )
        except ApiException as e:
            raise CustomApiException(e)

        return KernelsPage(list_response)

    def list_all_kernels(self) -> List[Kernel]:
        """
        List all kernels.

        Returns:
            List of Kernels
        """
        all_kernels: List[Kernel] = []
        next_page_token = ""
        while True:
            kernel_list = self.list_kernels(
                page_size=0,
                page_token=next_page_token,
            )
            all_kernels = all_kernels + kernel_list.kernels
            next_page_token = kernel_list.next_page_token
            if next_page_token == "":
                break

        return all_kernels

    def update_kernel(
            self,
            kernel: Kernel,
            update_mask: str = "*",
    ) -> Kernel:
        """Updates a kernel.

        Args:
            kernel (Kernel): Kernel object with to-be-updated values.
            update_mask (str): Comma separated paths referencing which fields to update.
                Update mask must be non-empty.
                Allowed field paths are: {"display_name", "type", "image", "cpu_request", "cpu_limit", "gpu_resource_name",
                "gpu_request", "gpu_limit", "memory_bytes_request", "memory_bytes_limit", "yaml_pod_template_spec"}.

        Returns:
            Kernel: Updated Kernel object.
        """
        updated_api_object: V1Kernel

        try:
            updated_api_object = self.api_instance.kernel_service_update_kernel(
                kernel_name=f"kernels/{kernel.kernel_id}",
                kernel=kernel.to_api_object(),
                update_mask=update_mask,
            ).kernel
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_object(api_object=updated_api_object)

    def delete_kernel(self, kernel_id: str) -> None:
        """Deletes a kernel.

        Args:
            kernel_id (str): Kernel ID.
        """
        try:
            self.api_instance.kernel_service_delete_kernel(
                name=f"kernels/{kernel_id}",
            )
        except ApiException as e:
            raise CustomApiException(e)