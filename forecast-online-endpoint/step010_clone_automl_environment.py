from azureml.core import Workspace, Environment

ws = Workspace.from_config()

curated_env = Environment.get(ws, "AzureML-AutoML")
print(curated_env)

clonedautoml = curated_env.clone("clonedautoml")
clonedautoml.register(ws)
