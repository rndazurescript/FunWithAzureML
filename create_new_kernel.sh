#!/bin/bash

# Based on
# https://docs.microsoft.com/en-us/azure/machine-learning/how-to-run-jupyter-notebooks#add-new-kernels

# In a terminal run:
# chmod +x ./create_new_kernel.sh
# ./create_new_kernel.sh

# We will create a new conda environment named new_environment and we will make it visible
conda create -y --name new_environment pip ipykernel 

# Invoke the python from the new environment (instead of activating conda till https://github.com/conda/conda/issues/7980 closes )
/anaconda/envs/new_environment/bin/python -m ipykernel install --user --name new_kernel --display-name "New Python Kernel (new_environment)"

# List all available kernels
jupyter kernelspec list

# Delete a kernel
jupyter kernelspec remove new_kernel