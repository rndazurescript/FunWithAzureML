# Convert to onnx
# Pick you sample conversion code from https://reposhub.com/python/deep-learning/onnx-tutorials.html
import argparse
import os
import lightgbm as lgb
import onnxmltools
import joblib

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

target_model_name = f"churn_model_onnx_{args.country}"

output_onnx_model = f"{input_path}/{target_model_name}.onnx"

# Load the LightGBM model
lgb_model = joblib.load(f"{input_path}/model.joblib")

# Convert the LightGBM model into ONNX
# The initial_types argument is a python list.
# Each element is a tuple of a variable name and a type defined in onnxconverter_common/data_types.py
onnx_model = onnxmltools.convert_lightgbm(
    lgb_model, initial_types=[(variable_name, data_type), (variable_name, data_type)]
)

# Save as protobuf
onnxmltools.utils.save_model(onnx_model, output_onnx_model)
