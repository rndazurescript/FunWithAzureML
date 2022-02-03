import argparse
import os
import requests
from azure.identity import ManagedIdentityCredential

parser = argparse.ArgumentParser("train")
# This is the only thing you need
parser.add_argument("--data", type=str, help="Path to data")
# The following arguments are added to show you how to grab an access token and use the rest API
parser.add_argument(
    "--adls_account_name",
    type=str,
    help="The ADLS Account Name",
    default="dataingeststg",
)
parser.add_argument(
    "--adls_container", type=str, help="The ADLS container", default="adlsgen2"
)
parser.add_argument(
    "--adls_path",
    type=str,
    help="The ADLS container",
    default="folder-with-default-acl-applied/data/",
)

args = parser.parse_args()

# The files of the dataset are mounted locally and you can list them
print(f"Files in {args.data}:")
arr = os.listdir(args.data)
# This would print all the files and directories
for f in arr:
    print(f)


# You can also grab an access token to talk to the datalake dfs endpoint, using the managed identity of the cluster
client_id = os.environ.get("DEFAULT_IDENTITY_CLIENT_ID")
print(f"cliend id: {client_id}")
credential = ManagedIdentityCredential(client_id=client_id)
token = credential.get_token("https://datalake.azure.net/")

# List the files in the ADSL path
listdirUrl = f"https://{args.adls_account_name}.dfs.core.windows.net/{args.adls_container}?resource=filesystem&directory={args.adls_path}&recursive=false"
headers = {"Authorization": f"Bearer {token.token}", "x-ms-version": "2018-11-09"}
resp = requests.get(url=listdirUrl, headers=headers)
files_response = resp.json()
print("Files within ADLS")
print(files_response)


# Following doesn't work so probably managed identity works a bit different in the Azure Batch context
tokenUrl = f"http://169.254.169.254/metadata/identity/oauth2/token?client_id={client_id}&api-version=2018-02-01&resource=https%3A%2F%2Fdatalake.azure.net%2F"
print(tokenUrl)
headers = {"Metadata": "true"}
resp = requests.get(url=tokenUrl, headers=headers)
response_json = resp.json()
print("Response from IMDS")
print(response_json)
