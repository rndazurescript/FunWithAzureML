# Training based on
# https://github.com/microsoft/LightGBM/blob/master/examples/python-guide/advanced_example.py

import pandas as pd

import argparse
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
train_data = joblib.load(os.path.join(input_path, 'train_dataset.joblib'))
test_data = joblib.load(os.path.join(input_path, 'test_dataset.joblib'))


#
# Train the model
#

def log_metrics():
    from azureml.core.run import Run, _OfflineRun
    run = Run.get_context()
    isOffline = (type(run) == _OfflineRun)

    def callback(env):
        if not isOffline:
            # Log metric for this itteration (in this case auc as defined in the parameters)
            # https://github.com/microsoft/LightGBM/blob/742d72f8bb051105484fd5cca11620493ffb0b2b/python-package/lightgbm/callback.py#L71
            run.log(env.evaluation_result_list[0][1], env.evaluation_result_list[0][2])

    callback.after_iteration = True
    callback.order = 0
    return callback


# Based on AutoML ExtremeRandomTrees seems to perform well
# We will use https://github.com/microsoft/LightGBM/pull/2671
metric = 'auc'
parameters = {
    'application': 'binary',
    'objective': 'binary',
    'metric': metric,
    'is_unbalance': 'true',
    'num_leaves': 31,
    'feature_fraction': 0.5,
    'learning_rate': 0.05,
    'verbose': 0,
    'extra_trees': 'true',
    'boosting': 'rf',  # The original code was using gbdt
    'bagging_freq': 1,
    'bagging_fraction': 0.8,
}

results = {}
validation_set_name = 'test_dataset'  # The name that will appear in the evaluation results
model = lgb.train(parameters,
                  train_data,
                  valid_sets=test_data,
                  valid_names=[validation_set_name],
                  num_boost_round=5000,
                  early_stopping_rounds=100,
                  callbacks=[log_metrics()],
                  evals_result=results
                  )

# Store results as json
import json
with open(os.path.join(output_path, "evaluation_results.json"), "w") as write_file:
    json.dump(results, write_file)

# Store info for tagging the model
from datetime import datetime
tags = {
    'metric': metric,
    'best_score': model.best_score[validation_set_name][metric],
    'best_iteration': model.best_iteration,
    'trained_date': datetime.now().isoformat(),
}
with open(os.path.join(output_path, "model.tags.json"), "w") as write_file:
    json.dump(tags, write_file)

# Store feature importance as csv
feature_importance = pd.DataFrame(
    list(zip(model.feature_name(), model.feature_importance())),
    columns=['feature', 'importance'])
feature_importance.to_csv(os.path.join(output_path, 'model.feature_importance.csv'), index=False)

# Store actual model as joblib dump
joblib.dump(value=model, filename=os.path.join(output_path, 'model.joblib'))

print(f"Stored model and metadata in {output_path}")
