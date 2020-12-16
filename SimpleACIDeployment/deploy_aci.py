from azureml.core import Workspace, Model, Environment
from azureml.core.model import InferenceConfig
from azureml.core.webservice import AciWebservice

model_name = "churn_model_GR"
service_name = 'full-model-test'
score_filename = "score.py"

ws = Workspace.from_config()
env = Environment.from_conda_specification(
                   name="simple_env",
                   file_path="conda_env.yaml")
inference_config = InferenceConfig(entry_script=score_filename,
                                   environment=env)
aci_config = AciWebservice.deploy_configuration(cpu_cores=1,
                                                memory_gb=1)
model = Model(workspace=ws, name=model_name)
service = Model.deploy(workspace=ws,
                       name=service_name,
                       models=[model],
                       inference_config=inference_config,
                       deployment_config=aci_config,
                       overwrite=True)

service.wait_for_deployment(show_output=True)
