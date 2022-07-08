# Forecasting with online-endpoint

Behind the vnet, you will have to clony your own [AzureML-AutoML image](https://ml.azure.com/environments/AzureML-AutoML/version/115).

1. Run `step010_clone_automl_environment.py`.
1. In your custom environments you should have a new environment registered, named `clonedautoml`.

[Optionally] Build a new machine learning model, to replace the ones in this repo:

1. Use `step020_generate_dataset.py` to generate your own dataset.
1. Run an automl forecasting experiment
1. Download the `model.pkl` file from the trained model's `output` folder and place it in the `model` folder.
1. Download the `scoring_file_v_2_0_0.py` from the trained model's `output` folder and place it in the `score` folder.

Deploy the model:

1. Modify the `deployment.yml` to update:
   1. `your-deployment-name` to whatever you want to name your endpoint.
   1. `your-endpoint-name` to match an endpoint that you have already deployed
1. Deploy the endpoint locally to test:
   ```
   az ml online-deployment create --local -f deployment.yml
   ```
   If this fails you can get logs:
   ```
   az ml online-deployment get-logs --local -n your-deployment-name -e your-endpoint-name
   ```
   If you want to run the docker image locally to inspect you can do:
   ```
   docker image list | grep your-deployment-name
   docker run -it <IMAGE_ID_FROM_PREVIOUS_CMD> /bin/bash
   ```
   Or you can commit the failed instance and inspect that (which will contain the environment variables):
   ```
   docker ps -a | grep your-deployment-name
   docker commit <INSTANCE_ID_FROM_PREVIOUS_CMD> failed:v1
   docker run -it failed:v1 /bin/bash
   ```
1. Deploy the endpoint to a managed online one:
   ```
   az ml online-deployment create -f deployment.yml
   ```

> Note: If you are behind a vnet you need to add the following line in your deployment.yml file:
egress_public_network_access: disabled
See [the azureml examples](https://github.com/Azure/azureml-examples/tree/main/cli/endpoints/online/managed/vnet/sample) on the settings you need to specify for the endpoint and the deployment.

## Building custom docker images

You can build your own docker images and push them to your container registry using these steps:

1. In a command line navigate in a folder that contains a `Dockerfile`.
1. Build the docker image where you should replace `your-acr-name` with your Azure Container Registry's name (ACR):
   ```
   docker build . -t your-acr-name.azurecr.io/repo/customimagename:v1
   ```
1. Login to your ACR with the following command:
   ```
   docker login your-acr-name.azurecr.io
   ```
   You will find the username (it's `your-acr-name`) and the password in the `Access keys` section of your ACR.
1. Push the build image to your ACR:
   ```
   docker push your-acr-name.azurecr.io/repo/customimagename:v1
   ```
