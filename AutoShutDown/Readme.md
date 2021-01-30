# Auto shutdown AzureML resources

Have you made ACI deployments from AutoML or spined up compute instances that you forgot to shut down? 

This pipeline automatically shuts down all Azure Container Instances located in the same resource group as my AzureML workspace and all compute instances running in the workspace on a daily schedule.

You need to authorize the managed identity of the compute cluster to be able to perform these actions.


Start from the [jupiter notebooks that creates the pipeline](./ScheduleAutoShutdown.ipynb)