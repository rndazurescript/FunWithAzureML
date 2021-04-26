# Simple churn model based on LightGBM

Code based on [this example](https://www.kaggle.com/ezietsman/simple-python-lightgbm-example)
Dataset based on [telco churn dataset](https://www.kaggle.com/blastchar/telco-customer-churn)

## Data structure

Assume you have a data store (blob storage) and the data are stored in the following format:

```
{country_code}/{Year}/{Month}/{Day}/CustomerInfo.parquet
```

Columns:

- id: Customer Id
- customer_tenure: How many years the customer has subscribed
- product_tenure: How long is the customer in the specific product
- activity_last_6_months: Minutes talked on phone last 6 months in total
- activity_last_12_months: Minutes talked on phone last 12 months in total
- churned: Bool indicating if the customer churned

Normally we would also need monetary values as described in the [RFM marketing modeling](https://en.wikipedia.org/wiki/RFM_(market_research))

## Instructions

- Run `UploadDataset.ipynd` to upload sample to default datastore
- [Optionally] Execute all python `step_*` files to run the training process locally
- Run `CreateTrainingPipeline.ipynb` to register the training pipeline that takes country as a parameter
- Execute the training pipeline to register a model


## TODOs

- Convert [model to onnx]](https://github.com/onnx/onnxmltools) and inference using ml.net


## Things that could be done better

The following best practices were not followed in order to simplify the examples:

- Separate code in folders. Currently we are uploading everything in all step snapshots which also reduces reusability of previously executed steps.
- Convert `CreateTrainingPipeline.ipynd` to [production ready python code](https://docs.microsoft.com/en-us/azure/machine-learning/tutorial-convert-ml-experiment-to-production). We wanted to document the steps etc but normally this is a python script which is executed after each git push ([Continuous Deployment](https://en.wikipedia.org/wiki/Continuous_deployment)).

