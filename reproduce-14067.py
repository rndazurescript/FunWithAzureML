# Sample code to reproduce timeout issue described in
# https://github.com/Azure/azure-sdk-for-python/issues/14067

# Run mitmproxy and enter interceptions mode 
# > type i  and then specify .*
# Allow the first request to AAD to pass hitting A or double a

mitm_proxy= "http://127.0.0.1:8080"
container_name= "issue14067"
blob_to_read = "debug.log"

# Configure a proxy
# https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-configure-proxy?tabs=cmd
import io
from io import BytesIO
import os
os.environ["HTTP_PROXY"] = mitm_proxy
os.environ["HTTPS_PROXY"] = mitm_proxy

# Retrieve the storage account and the storage key
import json
settings= {}
with open('./settings.json') as f:
    settings = json.load(f)
account_name = settings["STORAGE_ACCOUNT_NAME"]

# Configure identity that has "Storage Blob Data Reader" access
os.environ["AZURE_CLIENT_ID"] = settings["AZURE_CLIENT_ID"]
os.environ["AZURE_CLIENT_SECRET"] = settings["AZURE_CLIENT_SECRET"]
os.environ["AZURE_TENANT_ID"] = settings["AZURE_TENANT_ID"]

# Create the client
from azure.storage.blob.aio import (
    BlobServiceClient,
    ContainerClient,
    BlobClient,
)
from azure.core.exceptions import (
    ResourceNotFoundError,
    ClientAuthenticationError
)
from azure.identity.aio import DefaultAzureCredential

async def download_blob_using_blobservice(account_name: str, credential: DefaultAzureCredential, container_name:str , blob_name: str, file_stream: io.BytesIO):
    try:
        # Timeout didn't work on this code...
        blob_service = BlobServiceClient(f"{account_name}.blob.core.windows.net", credential=credential, connection_timeout=1, read_timeout=1)
        blob_client = blob_service.get_blob_client(container_name, blob_name)
        storage_stream_downloader = await blob_client.download_blob()
        await storage_stream_downloader.readinto(file_stream)
        return
    except ResourceNotFoundError:
        raise KeyError(blob_name)
    except ClientAuthenticationError:
        raise


async def download_blob_using_blobclient(account_name: str, credential:DefaultAzureCredential, container_name:str , blob_name: str, file_stream: io.BytesIO):
    try:
        blob_client = BlobClient(f"{account_name}.blob.core.windows.net", credential=credential, container_name=container_name, blob_name=blob_name, connection_timeout=1, read_timeout=1)
        storage_stream_downloader = await blob_client.download_blob()
        await storage_stream_downloader.readinto(file_stream)
        return
    except ResourceNotFoundError:
        raise KeyError(blob_name)
    except ClientAuthenticationError:
        raise

# Execute method
from io import (
    BytesIO,
    TextIOWrapper
)
import asyncio

def execute_code(loop, timeout=None):
    with BytesIO() as file_stream:
        service_principal = DefaultAzureCredential(exclude_cli_credential=True)
        future = asyncio.run_coroutine_threadsafe(
            download_blob_using_blobclient(account_name,service_principal, container_name, blob_to_read, file_stream),
            loop=loop)
        future.result(timeout)
        file_stream.flush()
        file_stream.seek(0)
        bw=TextIOWrapper(file_stream).read()
        print(bw)
        return

loop = asyncio.get_event_loop()
future = loop.run_in_executor(None, execute_code, loop)
loop.run_until_complete(future)