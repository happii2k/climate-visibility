from azure.storage.blob import BlobServiceClient
import os
from src.constant import *

class AzureBlobClient:
    blob_service_client = None

    def __init__(self, connection_string=None):
        if AzureBlobClient.blob_service_client is None:
            if connection_string is None:
                connection_string = os.getenv(AZURE_STORAGE_CONNECTION_STRING_ENV_KEY)
            
            if connection_string is None:
                raise Exception(f"Environment variable '{AZURE_STORAGE_CONNECTION_STRING_ENV_KEY}' is not set.")

            # Initialize the BlobServiceClient once
            AzureBlobClient.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        self.blob_service_client = AzureBlobClient.blob_service_client

    # Example method to get a container client
    def get_container_client(self, container_name):
        return self.blob_service_client.get_container_client(container_name)

    # Example method to list blobs in a container
    def list_blobs(self, container_name):
        container_client = self.get_container_client(container_name)
        return [blob.name for blob in container_client.list_blobs()]
