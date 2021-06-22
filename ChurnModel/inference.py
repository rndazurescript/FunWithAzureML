import joblib
import logging
import pandas as pd
from os import path


class ChurnModel(object):
    def __init__(self, country=None, version=None):
        model_name = f"churn_model_{country}"
        model_directory = self._get_model_directory(model_name, version)
        model_path = path.join(model_directory, "model.joblib")
        self.model = joblib.load(model_path)
        logging.info(f"Model features: {self.model.feature_name()}")

    def _get_model_directory(self, model_name, version):
        model_directory = "./model"  # Load local if not attached to AzureML
        from azureml.core.model import Model
        from azureml.exceptions import ModelNotFoundException

        try:
            model_directory = Model.get_model_path(model_name, version=version)
        except ModelNotFoundException as e:
            logging.debug(e)
            logging.info("Could not load model from AzureML cache")
        logging.info(f"{model_name} location is {model_directory}")
        return model_directory

    def run(self, data):
        # Keep only the columns needed by the model
        X = data.filter(items=self.model.feature_name())
        y = self.model.predict(X)
        return y


# The following code will run if we invoke this file directly from
# command line, e.g. python inference.py
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
    model = ChurnModel()
    test_data = pd.DataFrame(
        {
            "id": ["loyal_user", "churning_user"],
            "customer_tenure": [32, 8],
            "product_tenure": [2, 8],
            "activity_last_6_months": [60, 12],
            "activity_last_12_months": [120, 14],
        },
        columns=[
            "id",
            "customer_tenure",
            "product_tenure",
            "activity_last_6_months",
            "activity_last_12_months",
        ],
    )
    print("Test dataset")
    print(test_data)
    result = model.run(test_data)
    # Add the user id to the resulted probability
    output = pd.DataFrame(
        zip(test_data["id"].values, result), columns=["id", "churn_probability"]
    )
    print("Results")
    print(output)
