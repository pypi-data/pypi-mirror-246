# Script to insert kernels into the database [as is 1.12.2023]

# Prerequisites: kubectl port-forward deployment/notebook 8080:8080 --namespace=notebook-system-dev

import h2o_authn

from h2o_notebook.clients.kernel.client import KernelClient
from h2o_notebook.clients.kernel.type import KernelType

super_admin_token = "INSERT HERE YOUR SUPER ADMIN PLATFORM TOKEN"
tp = h2o_authn.TokenProvider(refresh_token=super_admin_token, issuer_url="https://auth.cloud-dev.h2o.ai/auth/realms/hac-dev", client_id="hac-platform-public")

c = KernelClient(
    server_url="http://localhost:8080",
    token_provider=tp,
    verify_ssl=False,
)


c.create_kernel(
    kernel_id="python",
    display_name="Python",
    kernel_type=KernelType.TYPE_PYTHON,
    image="gcr.io/vorvan/h2oai/h2o-kernel-py:0.3.4",
    memory_bytes_limit="12884901888",
    memory_bytes_request="12884901888",
)

c.create_kernel(
    kernel_id="python-gpu",
    display_name="Python [GPU]",
    kernel_type=KernelType.TYPE_PYTHON,
    image="gcr.io/vorvan/h2oai/h2o-kernel-py-gpu:0.3.4",
    gpu_limit=1,
    gpu_request=1,
    cpu_limit=4,
    cpu_request=1,
    memory_bytes_limit="8589934592",
)

c.create_kernel(
    kernel_id="python-l",
    display_name="Python [L]",
    kernel_type=KernelType.TYPE_PYTHON,
    image="gcr.io/vorvan/h2oai/h2o-kernel-py:0.3.4",
    memory_bytes_limit="30064771072",
    memory_bytes_request="30064771072",
)

c.create_kernel(
    kernel_id="python-xl",
    display_name="Python [XL]",
    kernel_type=KernelType.TYPE_PYTHON,
    image="gcr.io/vorvan/h2oai/h2o-kernel-py:0.3.4",
    memory_bytes_limit="64424509440",
    memory_bytes_request="64424509440",
)

c.create_kernel(
    kernel_id="r",
    display_name="R",
    kernel_type=KernelType.TYPE_R,
    image="gcr.io/vorvan/h2oai/h2o-kernel-r:0.3.4",
    memory_bytes_limit="64424509440",
    memory_bytes_request="64424509440",
)

c.create_kernel(
    kernel_id="r-l",
    display_name="R [L]",
    kernel_type=KernelType.TYPE_R,
    image="gcr.io/vorvan/h2oai/h2o-kernel-r:0.3.4",
    memory_bytes_limit="173946175488",
    memory_bytes_request="173946175488",
)

c.create_kernel(
    kernel_id="python-spark",
    display_name="Spark - Python",
    kernel_type=KernelType.TYPE_SPARK_PYTHON,
    image="gcr.io/vorvan/h2oai/h2o-kernel-pyspark:0.3.4",
    memory_bytes_limit="12884901888",
    memory_bytes_request="12884901888",
)

c.create_kernel(
    kernel_id="r-spark",
    display_name="Spark - R",
    kernel_type=KernelType.TYPE_SPARK_R,
    image="gcr.io/vorvan/h2oai/h2o-kernel-sparkr:0.3.4",
    memory_bytes_limit="12884901888",
    memory_bytes_request="12884901888",
)

print(c.list_kernels())