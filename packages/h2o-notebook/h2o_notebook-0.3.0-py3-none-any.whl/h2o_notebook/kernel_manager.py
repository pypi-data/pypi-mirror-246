import os
import shutil
import time
from typing import Any

import grpc
from enterprise_gateway.services.kernels.remotemanager import RemoteMappingKernelManager

from h2o_notebook.gen.ai.h2o.notebook.v1.kernel_service_pb2 import GetKernelRequest
from h2o_notebook.gen.ai.h2o.notebook.v1.kernel_service_pb2 import ListKernelsRequest
from h2o_notebook.gen.ai.h2o.notebook.v1.kernel_service_pb2_grpc import (
    KernelServiceStub,
)


class NotebookRemoteMappingKernelManager(RemoteMappingKernelManager):
    def __init__(self, **kwargs):
        self.log.info("NotebookRemoteMappingKernelManager.__init__")
        addr = os.getenv("H2O_NOTEBOOK_SERVER_GRPC_ADDR")
        if not addr:
            raise ValueError("H2O_NOTEBOOK_SERVER_GRPC_ADDR environment variable is not set")

        channel = grpc.insecure_channel(addr)
        self.notebook_client = KernelServiceStub(channel)

        # Authorize GRPC requests with Kubernetes service account token if not disabled (local testing)
        # TODO: Support projected service account tokens (the token may update, so handle accordingly)
        self.request_metadata = []
        if os.getenv("NOTEBOOK_ENABLE_GRPC_AUTH", 'True').lower() == "false":
            self.log.info("GRPC auth is disabled")
        else:
            path = os.getenv("KUBERNETES_SERVICE_ACCOUNT_TOKEN_FILE", "/var/run/secrets/kubernetes.io/serviceaccount/token")
            self.request_metadata.append(('authorization', 'Bearer ' + read_file(path)))

        # Try calling an endpoint to verify the connection
        self.notebook_client.ListKernels(request=ListKernelsRequest(), metadata=self.request_metadata)

        super().__init__(**kwargs)

    async def start_kernel(self, *args: list[Any] | None, **kwargs: dict[str, Any] | None):
        kernel_name = kwargs["kernel_name"]
        self.log.info("NotebookRemoteMappingKernelManager.start_kernel: kernel_name=%s, kwargs=%s", kernel_name, kwargs)
        kernel = self.notebook_client.GetKernel(
            request=GetKernelRequest(
                name=kernel_name,
            ),
            metadata=self.request_metadata
        ).kernel

        # This is where we can modify kernel-pod.yaml.j2 file with data from kernel
        # For now, just create copy of the default file
        kernel_dir = f"/tmp/{kernel.name}"
        shutil.copytree("/opt/h2oai/gateway/scripts", f"{kernel_dir}", dirs_exist_ok=True)

        # Artificially delay
        time.sleep(2)
        return await super().start_kernel(**kwargs)


def read_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()
