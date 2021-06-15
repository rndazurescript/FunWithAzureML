import os
import csv
import argparse
from selenium import webdriver

# Retrieve arguments configured through script_params
parser = argparse.ArgumentParser()
parser.add_argument("--url", type=str, dest="url", help="The url to parse")
parser.add_argument(
    "--output-path",
    type=str,
    dest="output_path",
    help="directory to store results",
    default="./data",
)
args = parser.parse_args()

print(f"Parsing page {args.url}")
# Create output path if not exists
output_path = args.output_path
if not os.path.exists(output_path):
    os.makedirs(output_path)

# Initialize selenium
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome("/usr/local/bin/chromedriver", options=chrome_options)

# Go to url and pull links
driver.get(args.url)
links = driver.find_elements_by_tag_name("a")
link_list = []
for link in links:
    link_list.append([link.text, link.get_attribute("href")])

# Canonicalize output file name
output_file_name = f"{args.url}.csv"
for c in '\\/:*?"<>|':
    output_file_name = output_file_name.replace(c, "")

# Store in a csv file
with open(os.path.join(output_path, output_file_name), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(link_list)
