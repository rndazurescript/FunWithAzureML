#!/bin/bash

mkdir -p cfg

# Copy binary
cp darknet_repo/darknet ./

# Copy configuration
cp darknet_repo/cfg/coco.data cfg/
cp darknet_repo/cfg/yolov4.cfg  cfg/

# copy sample data
cp -r darknet_repo/data ./data