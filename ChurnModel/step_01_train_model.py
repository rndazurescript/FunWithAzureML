# Training based on
# https://github.com/microsoft/LightGBM/blob/master/examples/python-guide/advanced_example.py

import numpy as np
import pandas as pd

import argparse
import datetime
import os

# retrieve arguments configured through script_params in estimator
parser = argparse.ArgumentParser()
parser.add_argument('--input-path', type=str, dest='input_path', help='directory to load datasets', default='./data')
parser.add_argument('--output-path', type=str, dest='output_path', help='directory to store model', default='./model')
args = parser.parse_args()

input_path = args.input_path

# Create output path if not exists
output_path = args.output_path
if not os.path.exists(output_path):
  os.makedirs(output_path)

#
# Load the LightGBM data containers
#
import lightgbm as lgb
import joblib

print(f"Loading data from {input_path}")
train_data=joblib.load(os.path.join(input_path,'train_dataset.joblib'))
test_data=joblib.load(os.path.join(input_path,'test_dataset.joblib'))


#
# Train the model
#

def log_metrics():
    from azureml.core import Run, _OfflineRun
    run = Run.get_context()
    isOffline = (type(run) == _OfflineRun)

    def callback(env):
        if not isOffline:
            # Log AUC for this itteration
            # https://github.com/microsoft/LightGBM/blob/742d72f8bb051105484fd5cca11620493ffb0b2b/python-package/lightgbm/callback.py#L71
            run.log(env.evaluation_result_list[0][1],env.evaluation_result_list[0][2])

    callback.after_iteration = True
    callback.order = 0
    return callback


parameters = {
    'application': 'binary',
    'objective': 'binary',
    'metric': 'auc',
    'is_unbalance': 'true',
    'boosting': 'gbdt',
    'num_leaves': 31,
    'feature_fraction': 0.5,
    'bagging_fraction': 0.5,
    'bagging_freq': 20,
    'learning_rate': 0.05,
    'verbose': 0
}

model = lgb.train(parameters,
                       train_data,
                       valid_sets=test_data,
                       num_boost_round=5000,
                       early_stopping_rounds=100,
                       callbacks=[log_metrics()]
                       )

feature_importance = pd.DataFrame(
                             list(zip(model.feature_name(), model.feature_importance())),
                             columns=['feature','importance']
                             )
feature_importance.to_csv(os.path.join(output_path,'model.feature_importance.csv'), index=False)

joblib.dump(value=model, filename=os.path.join(output_path,'model.joblib'))


print(f"Stored model and metadata in {output_path}")
