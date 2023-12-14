import os

import grpc
from jupyter_client.kernelspec import KernelSpec
from jupyter_client.kernelspec import KernelSpecManager

from h2o_notebook.gen.ai.h2o.notebook.v1.kernel_pb2 import Kernel
from h2o_notebook.gen.ai.h2o.notebook.v1.kernel_service_pb2 import GetKernelRequest
from h2o_notebook.gen.ai.h2o.notebook.v1.kernel_service_pb2 import ListKernelsRequest
from h2o_notebook.gen.ai.h2o.notebook.v1.kernel_service_pb2_grpc import (
    KernelServiceStub,
)


class NotebookKernelSpecManager(KernelSpecManager):
    def __init__(self, **kwargs):
        self.log.info("NotebookKernelSpecManager.__init__")
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

    def get_all_specs(self):
        res = {}

        next_page_token = ""
        while True:
            kernel_list = self.notebook_client.ListKernels(
                request=ListKernelsRequest(
                    page_size=0,
                    page_token=next_page_token,
                ),
                metadata=self.request_metadata
            )

            for kernel in kernel_list.kernels:
                res[kernel.name] = {
                    "resource_dir": "",
                    "spec": self.__to_kernel_spec(kernel).to_dict()
                }

            next_page_token = kernel_list.next_page_token
            if next_page_token == "":
                break

        return res

    def get_kernel_spec(self, kernel_name) -> KernelSpec:
        return self.__to_kernel_spec(self.notebook_client.GetKernel(request=GetKernelRequest(name=kernel_name), metadata=self.request_metadata).kernel)

    @staticmethod
    def __to_kernel_spec(kernel: Kernel) -> KernelSpec:
        return KernelSpec(
            display_name=kernel.display_name,
            language=NotebookKernelSpecManager.__to_language(kernel.type),
            metadata={
                "process_proxy": {
                    "class_name": "enterprise_gateway.services.processproxies.k8s.KubernetesProcessProxy",
                    "config": NotebookKernelSpecManager.__build_config(kernel.type, kernel.image)
                }
            },
            env=NotebookKernelSpecManager.__build_env(kernel),
            argv=NotebookKernelSpecManager.__build_argv(kernel.name, kernel.type),
        )

    @staticmethod
    def __to_language(kernel_type: int) -> str:
        if kernel_type in (Kernel.TYPE_PYTHON, Kernel.TYPE_SPARK_PYTHON):
            return "python"
        elif kernel_type in (Kernel.TYPE_R, Kernel.TYPE_SPARK_R):
            return "R"
        else:
            raise ValueError("Unknown kernel type: " + str(kernel_type))

    @staticmethod
    def __build_config(kernel_type: int, image:str) -> {}:
        cfg = {"image_name": image}
        if kernel_type in (Kernel.TYPE_SPARK_R, Kernel.TYPE_SPARK_PYTHON):
            cfg["executor_image_name"] = "gcr.io/vorvan/h2oai/h2o-kernel-pyspark:0.3.4"

        return cfg

    @staticmethod
    def __build_env(kernel: Kernel) -> {}:
        env = {}
        if kernel.type in (Kernel.TYPE_SPARK_R, Kernel.TYPE_SPARK_PYTHON):
            env["SPARK_HOME"] = "/opt/spark"
            env["SPARK_OPTS"] = "--master k8s://https://${KUBERNETES_SERVICE_HOST}:${KUBERNETES_SERVICE_PORT} --deploy-mode cluster --name ${KERNEL_USERNAME}-${KERNEL_ID} --conf spark.kubernetes.namespace=${KERNEL_NAMESPACE} --conf spark.kubernetes.driver.label.app=enterprise-gateway --conf spark.kubernetes.driver.label.kernel_id=${KERNEL_ID} --conf spark.kubernetes.driver.label.component=kernel --conf spark.kubernetes.executor.label.app=enterprise-gateway --conf spark.kubernetes.executor.label.kernel_id=${KERNEL_ID} --conf spark.kubernetes.executor.label.component=worker --conf spark.kubernetes.driver.container.image=${KERNEL_IMAGE} --conf spark.kubernetes.executor.container.image=${KERNEL_EXECUTOR_IMAGE} --conf spark.kubernetes.authenticate.driver.serviceAccountName=${KERNEL_SERVICE_ACCOUNT_NAME} --conf spark.kubernetes.submission.waitAppCompletion=false --conf spark.kubernetes.driverEnv.HTTP2_DISABLE=true --conf spark.scheduler.minRegisteredResourcesRatio=1 --conf spark.kubernetes.driver.annotation.cloud.h2o.ai/creator-display-name=${KERNEL_USER_NAME} --conf spark.kubernetes.driver.annotation.cloud.h2o.ai/owner-display-name=${KERNEL_USER_NAME} --conf spark.kubernetes.driver.label.cloud.h2o.ai/owner=${KERNEL_USER_SUB} --conf spark.kubernetes.driver.label.cloud.h2o.ai/creator=${KERNEL_USER_SUB} --conf spark.kubernetes.driver.label.telemetry.cloud.h2o.ai/include=true --conf spark.kubernetes.executor.annotation.cloud.h2o.ai/creator-display-name=${KERNEL_USER_NAME} --conf spark.kubernetes.executor.annotation.cloud.h2o.ai/owner-display-name=${KERNEL_USER_NAME} --conf spark.kubernetes.executor.label.cloud.h2o.ai/owner=${KERNEL_USER_SUB} --conf spark.kubernetes.executor.label.cloud.h2o.ai/creator=${KERNEL_USER_SUB} --conf spark.kubernetes.executor.label.telemetry.cloud.h2o.ai/include=true ${KERNEL_EXTRA_SPARK_OPTS}"
            env["HTTP2_DISABLE"] = "true"
            env["LAUNCH_OPTS"] = ""

        if kernel.memory_bytes_limit:
            env["KERNEL_MEMORY_LIMIT"] = str(kernel.memory_bytes_limit)
        if kernel.memory_bytes_request:
            env["KERNEL_MEMORY"] = str(kernel.memory_bytes_request)
        if kernel.cpu_limit:
            env["KERNEL_CPUS_LIMIT"] = str(kernel.cpu_limit)
        if kernel.cpu_request:
            env["KERNEL_CPUS"] = str(kernel.cpu_request)
        if kernel.gpu_limit:
            env["KERNEL_GPUS_LIMIT"] = str(kernel.gpu_limit)
        if kernel.gpu_request:
            env["KERNEL_GPUS"] = str(kernel.gpu_request)

        return env

    @staticmethod
    def __build_argv(kernel_name: str, kernel_type: int) -> []:
        if kernel_type in (Kernel.TYPE_PYTHON, Kernel.TYPE_R):
            return [
                "python",
                f"/tmp/{kernel_name}/launch_kubernetes.py",
                "--RemoteProcessProxy.kernel-id",
                "{kernel_id}",
                "--RemoteProcessProxy.port-range",
                "{port_range}",
                "--RemoteProcessProxy.response-address",
                "{response_address}",
                "--RemoteProcessProxy.public-key",
                "{public_key}"
            ]
        elif kernel_type == Kernel.TYPE_SPARK_PYTHON:
            return [
                f"/tmp/{kernel_name}/run-py.sh",
                "--RemoteProcessProxy.kernel-id",
                "{kernel_id}",
                "--RemoteProcessProxy.port-range",
                "{port_range}",
                "--RemoteProcessProxy.response-address",
                "{response_address}",
                "--RemoteProcessProxy.public-key",
                "{public_key}",
                "--RemoteProcessProxy.spark-context-initialization-mode",
                "lazy"
            ]
        elif kernel_type == Kernel.TYPE_SPARK_R:
            return [
                f"/tmp/{kernel_name}/run-r.sh",
                "--RemoteProcessProxy.kernel-id",
                "{kernel_id}",
                "--RemoteProcessProxy.port-range",
                "{port_range}",
                "--RemoteProcessProxy.response-address",
                "{response_address}",
                "--RemoteProcessProxy.public-key",
                "{public_key}",
                "--RemoteProcessProxy.spark-context-initialization-mode",
                "lazy"
            ]
        else:
            raise ValueError("Unknown kernel type: " + str(kernel_type))


def read_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()

