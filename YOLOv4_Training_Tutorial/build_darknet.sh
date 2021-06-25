#!/bin/bash

# Install opencv
sudo apt update
sudo apt install libopencv-dev python3-opencv

sudo cp /usr/local/cuda-10.2/include/* /usr/local/cuda/include/
sudo cp -r /usr/local/cuda-10.2/lib64/* /usr/local/cuda/lib64/

git clone https://github.com/AlexeyAB/darknet --depth 1

cd darknet
sed -i 's/OPENCV=0/OPENCV=1/' Makefile
sed -i 's/GPU=0/GPU=1/' Makefile
sed -i 's/CUDNN=0/CUDNN=1/' Makefile
sed -i 's/CUDNN_HALF=0/CUDNN_HALF=1/' Makefile

make

cd ..