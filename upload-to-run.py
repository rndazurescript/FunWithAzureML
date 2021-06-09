from azureml.core import Workspace, Experiment, Run

experiment_name = "experiment-name"
run_id = "the_run_id"

ws = Workspace.from_config()
experiment = Experiment(ws, experiment_name)

run = Run(experiment, run_id)

# HTML files like plottly render fine in the outputs
run.upload_file("test.html", "./test.html")
