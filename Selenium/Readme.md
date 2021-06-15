# Using selenium in AzureML pipelines to scrap data out of websites

This is a sample based on [an azure function selenium sample code](https://github.com/rebremer/azure-function-selenium). 

The idea is to create a custom selenium environment that will be able to run selenium based tasks and output the scrapped data in csv files in the [output file dataset](https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.data.outputfiledatasetconfig).

Start by reading the [notebook in this folder](Selenium_based_azureml_tasks.ipynb).

## The idea

- Create a docker image that contains Selenium.
- Create a python script that parses the page and outputs a csv.
- Use AzureML pipeline to orchestrate steps.
- Use blob storage to persist data.

## TODO

Perhaps move to [Edge driver](https://docs.microsoft.com/en-us/microsoft-edge/webdriver-chromium/?tabs=python) when selenium [supports it on linux](https://www.selenium.dev/documentation/en/webdriver/driver_requirements/):

```
# 1. Install Edge-Beta (root image is debian)
# See https://www.omgubuntu.co.uk/2021/01/how-to-install-edge-on-ubuntu-linux
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg \
    && install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/ \
    && sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge-dev.list' \
    && apt update -qqy && apt install microsoft-edge-beta \
    && rm microsoft.gpg && rm -rf /var/lib/apt/lists/* /var/cache/apt/*
```
