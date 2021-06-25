#!/bin/bash

# Install opencv
sudo apt update
sudo apt install libopencv-dev python3-opencv -y

# Copy the missing cudablas_v2.h from cuda-10.2
sudo cp /usr/local/cuda-10.2/include/* /usr/local/cuda/include/
sudo cp -r /usr/local/cuda-10.2/lib64/* /usr/local/cuda/lib64/