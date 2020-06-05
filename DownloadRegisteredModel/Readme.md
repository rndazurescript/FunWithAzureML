# Download a model in azure ml pipeline

Imagine that you have a model that you need to use in your inference pipeline. 

You can register the model in azureml and then you can download it in your python script.

To register the model [see this notebook](https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/deployment/deploy-to-cloud/model-register-and-deploy.ipynb):
``` python
from azureml.core import Model
from azureml.core.resource_configuration import ResourceConfiguration


model = Model.register(workspace=ws,
                       model_name='my-sklearn-model',                # Name of the registered model in your workspace.
                       model_path='./sklearn_regression_model.pkl',  # Local file to upload and register as a model.
                       model_framework=Model.Framework.SCIKITLEARN,  # Framework used to create the model.
                       model_framework_version='0.19.1',             # Version of scikit-learn used to create the model.
                       sample_input_dataset=input_dataset,
                       sample_output_dataset=output_dataset,
                       resource_configuration=ResourceConfiguration(cpu=1, memory_in_gb=0.5),
                       description='Ridge regression model to predict diabetes progression.',
                       tags={'area': 'diabetes', 'type': 'regression'})

print('Name:', model.name)
print('Version:', model.version)
```

To get the path of the model and load it from there:
``` python
from azureml.core.model import Model
from pathlib import Path

original_model_path = Model.get_model_path('my-sklearn-model')

raw_path = Path(original_model_path)

# Enumerate the artifacts that were pushed as part of the model
for path in raw_path.rglob('*'):
    print(path.name)

```