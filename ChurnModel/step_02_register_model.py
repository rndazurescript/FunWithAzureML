# Get the trained model and register it in the AzureML models section
import argparse
import os
import lightgbm as lgb

# retrieve arguments configured through script_params in estimator
parser = argparse.ArgumentParser()
parser.add_argument(
    "--input-path",
    type=str,
    dest="input_path",
    help="directory to load model",
    default="./model",
)
parser.add_argument(
    "--country", type=str, dest="country", help="Country used to train the model"
)
args = parser.parse_args()

input_path = args.input_path

target_model_name = f"churn_model_{args.country}"

from azureml.core import Workspace, Dataset, Model
from azureml.core.run import Run, _OfflineRun

run = Run.get_context()
ws = None
if type(run) == _OfflineRun:
    ws = Workspace.from_config()
else:
    ws = run.experiment.workspace

# Load metadata from the training process
import json

tags = {}
with open(os.path.join(input_path, "model.tags.json"), "r") as read_file:
    print("Converting JSON encoded tag data into Python dictionary")
    tags = json.load(read_file)
# Add pipeline metadata
tags["country"] = args.country
tags["type"] = "churn"

# Get reference to the training dataset to associate with model
training_ds = Dataset.get_by_name(ws, f"churn-training-{args.country}")

# Register the model
model = None
if type(run) == _OfflineRun:
    # If we are offline we don't have the run context to
    # associate with the model registration
    model = Model.register(
        ws,
        model_name=target_model_name,
        model_path=input_path,
        tags=tags,
        model_framework="LightGBM",
        model_framework_version=lgb.__version__,
        datasets=[("training data", training_ds)],
    )
else:
    # Associate the experiment and the run_id with this
    # model registration
    # We need to upload artifact first to the run
    run.upload_folder("model", input_path)
    model = run.register_model(
        model_name=target_model_name,
        model_path="model",
        tags=tags,
        model_framework="LightGBM",
        model_framework_version=lgb.__version__,
        datasets=[("training data", training_ds)],
    )

print(f"Registered version {model.version} for model {model.name}")
