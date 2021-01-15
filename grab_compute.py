"""
Sample code getting a reference to the compute target
"""
import argparse
import azureml
from azureml.core import Workspace


print("Azure ML SDK Version: ", azureml.core.VERSION)

parser = argparse.ArgumentParser()
parser.add_argument('--cluster-name', type=str, dest='cluster_name',
                    help='The cluster to look up in the workspace')
args = parser.parse_args()

# Connect to workspace and get resource references
ws = Workspace.from_config()
# Verify that cluster exists
# https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.core.workspace.workspace?view=azure-ml-py#compute-targets
cpu_cluster = ws.compute_targets.get(args.cluster_name)
if cpu_cluster is None:
    message = f'Cluster {args.cluster_name} does not exist'
    print(message)  # Or raise KeyError(message)
else:
    print(f'Found cluster {cpu_cluster.name}')

print('Exiting')
