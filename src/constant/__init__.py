from azure.storage.blob import BlobServiceClient
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
import os

# Replace with your connection string
AZURE_STORAGE_CONNECTION_STRING_ENV_KEY = os.getenv('connect_str')
container_name = "artifacts"  # Use your container name


# Create folder-like prefix using timestamp
artifact_folder_name = datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
blob_path = f"{artifact_folder_name}/model.pkl"



