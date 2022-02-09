import argparse
import shutil
from os import path, listdir

parser = argparse.ArgumentParser()
parser.add_argument("input", help="the input folder")
parser.add_argument("output", help="the output folder")
args = parser.parse_args()

# fetch all files
for file_name in listdir(args.input):
    # construct full file path
    source = path.join(args.input,file_name)
    destination = path.join(args.output,file_name)
    # copy only files
    if path.isfile(source):
        print(f'\tTrying to copy {source} to {destination}')
        shutil.copyfile(source, destination)
        print('\tCopied', file_name)


print("Done working!")