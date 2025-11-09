from azure.storage.blob import BlobServiceClient
from datetime import datetime

# Replace with your connection string
container_name = "artifacts"  # Use your container name

blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_client = blob_service_client.get_container_client(container_name)

# Create folder-like prefix using timestamp
artifact_folder_name = datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
blob_path = f"{artifact_folder_name}/model.pkl"



# Upload file
with open("model.pkl", "rb") as data:
    container_client.upload_blob(name=blob_path, data=data)

print(f"Model uploaded to blob path: {blob_path}")
