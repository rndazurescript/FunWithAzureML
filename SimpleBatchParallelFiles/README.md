# Simple parallel batch processing of multiple files

Sample to parallelize the processing of multiple files in a pipeline.

We have weather data partitioned by year and month e.g. `greece-weather-data/{year}/{month}/data.parquet`. The input dataset is a pipeline parameter and can change.

We want to batch process them all in the `cpu-cluster` in 10 processes, 5 on each node.
Each process will be invoked multiple times, passing in 10 files every time.
The script will print which files it's processing every time.

Results will be stored in `inferences/greece-weather/outputs.txt` file.
