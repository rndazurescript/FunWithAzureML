# This file was exported from a notebook
# And then we added the parsers to parse arguments
# instead of having hard coded file names in the 
# notebook.
#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import os
import argparse
import pandas

# Retrieve arguments configured through script_params
parser = argparse.ArgumentParser()
parser.add_argument(
    "--company-file",
    type=str,
    dest="company_file",
    help="The excel that contains the company info",
    default="company1.xlsx",
)
parser.add_argument(
    "--output-path",
    type=str,
    dest="output_path",
    help="directory to store results",
    default="./output",
)
parser.add_argument(
    "--output-file-name",
    type=str,
    dest="output_file_name",
    help="The name of the csv to store",
    default="company1.csv",
)
args = parser.parse_args()

print(f"Reading excel file {args.company_file}")
# Create output path if not exists
output_path = args.output_path
if not os.path.exists(output_path):
    os.makedirs(output_path)

# HERE STARTS THE PROCESSING

# Let's create a simple dataframe
lst = ["Geeks", "For", "Geeks", "is", "portal", "for", "Geeks"]
df = pandas.DataFrame(lst)


# HERE STORE IN THE output_path folder
df.to_csv(os.path.join(output_path, args.output_file_name), index=False)
