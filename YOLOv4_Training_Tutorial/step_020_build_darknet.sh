#!/bin/bash

darknetFolder=./darknet_repo

if [ ! -d "$darknetFolder" ]; then
  # If repo is not cloned yet
  # Clone the repo without bringing in the history
  git clone https://github.com/AlexeyAB/darknet --depth 1 $darknetFolder
  cd darknet_repo
else
  # Pull latest
  cd $darknetFolder
  git pull
fi

sed -i "s/OPENCV=0/OPENCV=1/" Makefile
sed -i "s/GPU=0/GPU=1/" Makefile
sed -i "s/CUDNN=0/CUDNN=1/" Makefile
sed -i "s/CUDNN_HALF=0/CUDNN_HALF=1/" Makefile

# Add cuda in the path as it is not in the kernel's PATH
export PATH="$PATH:/usr/local/cuda/bin"
echo $PATH 

make

cd ..
