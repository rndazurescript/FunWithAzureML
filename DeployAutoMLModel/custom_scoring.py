# Based on the original generated automl code
# Adapted based on:
# https://docs.microsoft.com/en-us/azure/machine-learning/how-to-machine-learning-interpretability-automl
import logging
import os
import numpy as np
import pandas as pd
import joblib

from azureml.train.automl.runtime.automl_explain_utilities import (
    automl_setup_model_explanations,
)

from azureml.automl.core.shared import logging_utilities, log_server
from azureml.telemetry import INSTRUMENTATION_KEY

from inference_schema.schema_decorators import input_schema, output_schema
from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType
from inference_schema.parameter_types.pandas_parameter_type import PandasParameterType
from inference_schema.parameter_types.standard_py_parameter_type import (
    StandardPythonParameterType,
)

try:
    log_server.enable_telemetry(INSTRUMENTATION_KEY)
    log_server.set_verbosity("INFO")
    logger = logging.getLogger("azureml.automl.core.scoring_script")
except Exception as e:
    logging_utilities.log_traceback(e, logger)
    pass


def init():
    global model, explainer
    # This mode name is available in environment variable
    model_name = os.getenv("model_name")
    if model_name is None:
        # If none we default to the name our scripts know
        model_name = "automl_diabetes"
        logger.warn(
            f"Environment variable model_name is not configured. Using hardcoded default value '{model_name}'"
        )
    model_directory = _get_model_directory(model_name)
    model_path = os.path.join(model_directory, "model.pkl")
    explainer_path = os.path.join(model_directory, "scoring_explainer.pkl")
    log_server.update_custom_dimensions({"model_name": model_name})
    try:
        logger.info(f"Loading model from path {model_path}.")
        model = joblib.load(model_path)
        logger.info("Loading model successful.")
        logger.info(f"Loading explainer from path {explainer_path}.")
        explainer = joblib.load(explainer_path)
        logger.info("Loading explainer successful.")
    except Exception as e:
        logging_utilities.log_traceback(e, logger)
        raise


def _get_model_directory(model_name, version=None):
    model_directory = "./outputs"  # Load local if not attached to AzureML
    from azureml.core.model import Model
    from azureml.exceptions import ModelNotFoundException

    try:
        model_directory = Model.get_model_path(model_name, version=version)
    except ModelNotFoundException as e:
        logger.debug(e)
        logger.info("Could not load model from AzureML cache")
    logger.info(f"{model_name} location is {model_directory}")
    return model_directory


input_sample = pd.DataFrame(
    {
        "0": pd.Series([0.0], dtype="float64"),
        "1": pd.Series([0.0], dtype="float64"),
        "2": pd.Series([0.0], dtype="float64"),
        "3": pd.Series([0.0], dtype="float64"),
        "4": pd.Series([0.0], dtype="float64"),
        "5": pd.Series([0.0], dtype="float64"),
        "6": pd.Series([0.0], dtype="float64"),
        "7": pd.Series([0.0], dtype="float64"),
        "8": pd.Series([0.0], dtype="float64"),
        "9": pd.Series([0.0], dtype="float64"),
    }
)
explain_output_sample = [
    {
        "0": -2.948,
        "1": 5.532,
        "2": -19.107,
        "3": -7.393,
        "4": -1.001,
        "5": 0.633,
        "6": -15.183,
        "7": -1.576,
        "8": -39.023,
        "9": -0.502,
    }
]
nested_input = StandardPythonParameterType(
    {
        "data": PandasParameterType(input_sample),
        "explain": StandardPythonParameterType(True),
    }
)

output_sample = np.array([0])
nested_output_data = StandardPythonParameterType(
    {
        "result": NumpyParameterType(output_sample),
        "explainations": StandardPythonParameterType(explain_output_sample),
        "error": "The error message if something has gone south",
    }
)


@input_schema("param", nested_input)
@output_schema(nested_output_data)
def run(param):
    try:
        data = param["data"]
        do_explain = param["explain"]
        result = model.predict(data)

        if do_explain:
            # Setup for inferencing explanations
            automl_explainer_setup_obj = automl_setup_model_explanations(
                model, X_test=data, task="regression"
            )
            # Retrieve model explanations for engineered explanations
            local_importance_values = explainer.explain(
                automl_explainer_setup_obj.X_test_transform
            )
            feature_names = list(model[0].get_column_names_and_types.keys())
            explainations = []
            # zip results
            for liv in local_importance_values:
                explainations.append(dict(zip(feature_names, liv)))

            return {"result": result.tolist(), "explainations": explainations}
        else:
            return {"result": result.tolist()}
    except Exception as e:
        result = str(e)
        return {"error": result}


# The following code will run if we invoke this file directly from
# command line, e.g. python custom_scoring.py
if __name__ == "__main__":
    # Set log level to debug
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # Create console handler and set level to just info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # Initialize model
    init()
    test_data = pd.DataFrame(
        {
            "0": [0.0380759064334241, -0.00188201652779104],
            "1": [0.0506801187398187, -0.044641636506989],
            "2": [0.0616962065186885, -0.0514740612388061],
            "3": [0.0218723549949558, -0.0263278347173518],
            "4": [-0.0442234984244464, -0.00844872411121698],
            "5": [-0.0348207628376986, -0.019163339748222],
            "6": [-0.0434008456520269, 0.0744115640787594],
            "7": [-0.00259226199818282, -0.0394933828740919],
            "8": [0.0199084208763183, -0.0683297436244215],
            "9": [-0.0176461251598052, -0.09220404962683],
        },
        columns=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    )
    print("Test dataset")
    print(test_data)
    result = run({"data": test_data, "explain": True})
    print("Results expected 151 and 75")
    print(result)
