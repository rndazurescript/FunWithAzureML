# Training based on
# https://github.com/microsoft/LightGBM/blob/master/examples/python-guide/advanced_example.py

import numpy as np
import pandas as pd

import argparse
import datetime
import os

# retrieve arguments configured through script_params in estimator
parser = argparse.ArgumentParser()
parser.add_argument('--country', type=str, dest='country', help='Country to train the model for')
parser.add_argument('--target-day', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), dest='target_day', help='The day to use for training')
parser.add_argument('--output-path', type=str, dest='output_path', help='directory to store results', default='./data')
args = parser.parse_args()

file_path="ChurnDataset/GR/2020/11/26"
if args.country is not None:
  if args.target_day is not None:
    file_path=f"ChurnDataset/{args.country}/{args.target_day.strftime('%Y/%m/%d')}"

print(f"Loading parquet from {file_path}")

# Create output path if not exists
output_path = args.output_path
if not os.path.exists(output_path):
  os.makedirs(output_path)

# We are using the default datastore but you could have used a different one as well
import azureml.core
from azureml.core import Workspace, Datastore, Dataset

ws = Workspace.from_config()
datastore = ws.get_default_datastore()

parquet_files = [(datastore, f"{file_path}/*.parquet")]
dataset = Dataset.Tabular.from_parquet_files(path=parquet_files)
train = dataset.to_pandas_dataframe()

# If you want clean up dataset here

# get the labels
y = train.churned.values

# and the features
train.drop(['id', 'churned'], inplace=True, axis=1)
x = train.values

#
# Create training and validation sets
#
from sklearn.model_selection import train_test_split
x, x_test, y, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)

#
# Create the LightGBM data containers
#
import lightgbm as lgb
train_data = lgb.Dataset(x, label=y, feature_name=train.columns.to_list())
test_data = lgb.Dataset(x_test, label=y_test, feature_name=train.columns.to_list())

import joblib
joblib.dump(value=train_data, filename=os.path.join(output_path,'train_dataset.joblib'))
joblib.dump(value=test_data, filename=os.path.join(output_path,'test_dataset.joblib'))

print(f"Prepared data in {output_path}")
