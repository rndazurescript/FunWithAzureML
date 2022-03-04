# Schedule a pipeline endpoint

**Problem statement**: You can schedule a published pipeline following (the docs instructions](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-trigger-published-pipeline#create-a-schedule).
The problem with this approach is that if the data scientist changes a component and publishes a new pipeline, they have to stop previous schedules and recreate them.

In this demo you will schedule an endpoint that was published for the [R forecasting pipeline created by custom components](../cli-v2-r-forecasting). Scheduling the endpoint and not the published pipeline allows the data scientist to replace the default pipeline ID of the endpoint when they feel that their code is stable enough to replace the existing scheduled execution.

Limitation: If the input parameters for the pipeline change, the schedule needs to be recreated to pass the additional parameters.
