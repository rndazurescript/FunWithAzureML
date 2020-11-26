# Training based on
# https://github.com/microsoft/LightGBM/blob/master/examples/python-guide/advanced_example.py
import argparse
import os
import lightgbm as lgb

# retrieve arguments configured through script_params in estimator
parser = argparse.ArgumentParser()
parser.add_argument('--input-path', type=str, dest='input_path', help='directory to load model', default='./model')
parser.add_argument('--country', type=str, dest='country', help='Country used to train the model')
args = parser.parse_args()

input_path = args.input_path

target_model_name=f"churn_model_{args.country}"

from azureml.core import Workspace, Model
ws = Workspace.from_config()
model = Model.register(ws, 
                        model_name=target_model_name, 
                        model_path=input_path, 
                        tags={ "country": args.country, "type": "churn" }, 
                        model_framework='LightGBM',
                        model_framework_version=lgb.__version__)


print(f"Registered version {model.version} for model  {model.name}")
