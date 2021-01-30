# The compute cluster has managed identity that needs to
# be able to shut down compute instances and scale down clusters
from azureml.core import Workspace
from azureml.core.run import Run, _OfflineRun
from azureml.core.compute import ComputeInstance, AmlCompute


# Get workspace
run = Run.get_context()
ws = None
if type(run) == _OfflineRun:
    ws = Workspace.from_config()
else:
    ws = run.experiment.workspace

# Use Managed Identity to authenticate
from azureml.core.authentication import MsiAuthentication
msi_auth = MsiAuthentication()

ws = Workspace(subscription_id=ws.subscription_id,
               resource_group=ws.resource_group,
               workspace_name=ws.name,
               auth=msi_auth)

# Loop through compute targets
for ct_name, ct in ws.compute_targets.items():
    if (isinstance(ct, ComputeInstance) and ct.get_status().state != "Stopped"):
        print(f"Stopping compute instance {ct.name}")
        try:
            ct.stop(wait_for_completion=False, show_output=False)
        except Exception as e:
            print(f"Failed to stop compute {ct.name} with error {e})")
    if (isinstance(ct, AmlCompute)):
        print(f"Scalling down cluster {ct.name}")
        try:
            ct.update(min_nodes=0)
        except Exception as e:
            print(f"Failed to scale down cluster {ct.name} with error {e})")
