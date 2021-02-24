#!/bin/bash
# Upgrade azureml-sdk
pip install --upgrade azureml-sdk
# Linting code
pip install --upgrade flake8
# Code formater
# For black, you may need to upgrade or remove enum34
# https://stackoverflow.com/questions/43124775/why-python-3-6-1-throws-attributeerror-module-enum-has-no-attribute-intflag
pip install --upgrade black