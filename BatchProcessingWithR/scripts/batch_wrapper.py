# Simple python wrapper to execute R scripts in batches
import subprocess
import os
import argparse

# Create variables used in this script
current_file_folder = os.path.dirname(os.path.abspath(__file__))
r_scipt_location = os.path.join(current_file_folder, "process_file.r")

parser = argparse.ArgumentParser()
parser.add_argument(
    "--r-output",
    type=str,
    dest="output_folder",
    help="Where to store the processed outputs in csv files",
    default="./output",
)
args, unknown_args = parser.parse_known_args()
print(f"Found extra args {unknown_args}")
output_path = args.output_folder
# Create output folder if it doesn't exist
if not os.path.exists(output_path):
    os.makedirs(output_path)


def init():
    print("Init function called")


def run(mini_batch):
    print(f"run method start: {__file__}, run({mini_batch})")
    resultList = []

    for file_path in mini_batch:
        print(f"Requesting to process file {file_path}")
        # Call R script for each file
        subprocess.check_call(
            ["Rscript", r_scipt_location, "-f", file_path, "-o", output_path]
        )
        print("R script called")
        resultList.append("Processed : {}".format(file_path))

    return resultList


# The following code will run if we invoke
# this file directly from console
if __name__ == "__main__":
    init()
