#!/bin/bash

mkdir -p cfg
mkdir -p data

# Copy binary
cp darknet_repo/darknet ./

# Copy configuration
cp darknet_repo/cfg/coco.data cfg/
cp darknet_repo/cfg/yolov4.cfg  cfg/

# Copy sample data
cp darknet_repo/data/person.jpg data/