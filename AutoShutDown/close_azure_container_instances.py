# The compute cluster has managed identity that will be used to shut down the ACI
# that may be spinned up from the AutoML interface
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azureml.core import Workspace
from azureml.core.run import Run, _OfflineRun
# ContainerInstanceManagementClient has not been updated to the new Auth model
# so we use a wrapper instead of DefaultAzureCredential
from cred_wrapper import CredentialWrapper
# from azure.identity import DefaultAzureCredential


# Get workspace
run = Run.get_context()
ws = None
if type(run) == _OfflineRun:
    ws = Workspace.from_config()
else:
    ws = run.experiment.workspace

# Get where this workspace is located
subscription_id = ws.subscription_id
resource_group = ws.resource_group

# Acquire a credential object
credential = CredentialWrapper()  # DefaultAzureCredential()

# https://docs.microsoft.com/en-us/python/api/azure-mgmt-containerinstance/azure.mgmt.containerinstance.containerinstancemanagementclient?view=azure-python
aci_client = ContainerInstanceManagementClient(credential, subscription_id)

# https://azuresdkdocs.blob.core.windows.net/$web/python/azure-mgmt-containerinstance/2.0.0/azure.mgmt.containerinstance.operations.html#azure.mgmt.containerinstance.operations.ContainerGroupsOperations
container_groups = aci_client.container_groups.list_by_resource_group(resource_group)
for container_group in container_groups:
    print(f"Stopping {container_group.name}")
    aci_client.container_groups.stop(resource_group, container_group.name)
