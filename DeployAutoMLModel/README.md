# Deploy an AutoML model with explainer

Sample code to deploy an autoML model in ACI.

Start by [training a model](TrainModel.ipynb) then [create explainer and register model](RegisterModel.ipynb) and finally [deploy registered model in ACI](DeployModel.ipynb).


The training process is logged under the `auto-ml-deployment-experiment` experiment. Model is register under the `automl_diabetes` name.

To test the model use and [online service](https://reqbin.com/) with the following headers:

```
POST /score HTTP/1.1
Authorization: Bearer yourkeyhere
Host: you-aci-name.your-region.azurecontainer.io
Content-Type: application/json
```

And the following payload:

```
{
  "param": {
          "data": [
            {
             "0": 0.0380759064334241,
             "1": 0.0506801187398187,
             "2": 0.0616962065186885, 
             "3": 0.0218723549949558, 
             "4": -0.0442234984244464,
             "5": -0.0348207628376986, 
             "6": -0.0434008456520269,
             "7": -0.00259226199818282,
             "8": 0.0199084208763183,
             "9": -0.0176461251598052
            },
            {
             "0":  -0.00188201652779104,
             "1": -0.044641636506989,
             "2": -0.0514740612388061,
             "3": -0.0263278347173518,
             "4":  -0.00844872411121698,
             "5": -0.019163339748222,
             "6": 0.0744115640787594,
             "7":  -0.0394933828740919,
             "8":  -0.0683297436244215,
             "9": -0.09220404962683
            }
          ],
          "explain": true
        }
}
```

Result should have the following format:
```
{
    "result": [194.8239283836361, 72.20494744027758],
    "explainations": [{
        "0": 3.4724164541111615,
        "1": -5.761159503199356,
        "2": 29.11932798184727,
        "3": -5.267926030307573,
        "4": 1.369984502566305,
        "5": 0.16520037531388615,
        "6": 5.421768261659971,
        "7": -1.01926685802043,
        "8": 16.880901077243024,
        "9": -0.15354731976074049
    }, {
        "0": -2.9486165130208173,
        "1": 5.53204928279358,
        "2": -19.10782189796979,
        "3": -7.393435495283295,
        "4": -1.0014481748239867,
        "5": 0.633218568165595,
        "6": -15.183526428766363,
        "7": -1.5769036298948877,
        "8": -39.023088815122826,
        "9": -0.5026363277277882
    }]
}
```

You can also view the swagger file with GET at `http://you-aci-name.your-region.azurecontainer.io/swagger.json`.