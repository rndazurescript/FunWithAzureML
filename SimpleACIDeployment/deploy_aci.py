from azureml.core import Workspace, Model, Environment
from azureml.core.model import InferenceConfig
from azureml.core.webservice import AciWebservice

service_name = "static-score"
score_filename = "score.py"

ws = Workspace.from_config()
env = Environment.from_conda_specification(
    name="simple_env", file_path="conda_env.yaml"
)
inference_config = InferenceConfig(entry_script=score_filename, environment=env)
aci_config = AciWebservice.deploy_configuration(
    cpu_cores=1,
    memory_gb=1,
    # For vnet integration add the following.
    # Use a subnet that is delegated to
    # Microsoft.ContainerInstance/containerGroups
    # vnet_name='private-endpoint-vnet',
    # subnet_name='delegated-subnet',
)
service = Model.deploy(
    workspace=ws,
    name=service_name,
    models=[],
    inference_config=inference_config,
    deployment_config=aci_config,
    overwrite=True,
)
try:
    service.wait_for_deployment(show_output=True)
except:
    print("Is your ACR publicly accessible?")
    service.get_logs()
