# Interesting scripts on AzureML

Most of them are not tested but still interesting enough to document.


## ONNX model from automl

```
from azureml.core import Run
from azureml.pipeline.core import PipelineRun
from azureml.train.automl.run import AutoMLRun
run = Run.get_context()
pipeline_run = PipelineRun(run.experiment, run.parent.id)
automl_run = pipeline_run.find_step_run("name-of-automl-step")[0]
automl_run = AutoMLRun(automl_run.experiment, automl_run.id)
best_run, model = automl_run.get_output(return_onnx_model=True)
```

## SQL ODBC and pyodbc driver on compute instance

Check that odbc driver is installed and then install through conda and upgrade through pip.

``` bash
dpkg -l | grep odbc
conda install pyodbc
pip install --upgrade pyodbc
```

![ODBC is installed](InterestingSnippets,OdbcDriversInstalledInCI.png)

## Shutdown compute instance on idle

See the work done in:

- https://github.com/matteote/azureml_shutdown_idle_compute_instances/blob/master/scripts/get_compute_instance_info.py
- https://github.com/csiebler/aml-compute-instance-snippets/blob/master/shutdown-if-inactive/shutdown_if_inactive.py

Schedule the execution of such a script through cron, in the [compute instance setup script](https://github.com/Azure/azureml-examples/tree/main/setup-ci). 