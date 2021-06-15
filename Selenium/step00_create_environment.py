import argparse
from azureml.core import Environment, Workspace

# Retrieve arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "--env-name",
    type=str,
    dest="name",
    help="The environment name to register",
    default="selenium-env",
)
args = parser.parse_args()

ws = Workspace.from_config()
# We are using a docker file located next to this notebook to create an environment
# to be able to run our tasks
env = Environment.from_dockerfile(
    name=args.name, dockerfile="AzureML-Selenium-Dockerfile"
)
env.register(ws)
env.build(ws).wait_for_completion(show_output=True)
