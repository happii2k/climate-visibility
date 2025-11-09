from datetime import datetime
import os

from dotenv import load_dotenv
load_dotenv()
import urllib.parse

username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")

username_escaped = urllib.parse.quote_plus(username)
password_escaped = urllib.parse.quote_plus(password)


 #"visibility-bucket-im"
MONGO_DATABASE_NAME = "visibility"
MONGODB_URL =  mongodb_url =  (
    f"mongodb+srv://{username_escaped}:{password_escaped}@visibility.global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
)

TARGET_COLUMN = "VISIBILITY"
CLUSTER_LABEL_COLUMN = "Cluster"

MODEL_FILE_NAME = "model"
MODEL_FILE_EXTENSION = ".pkl"

artifact_folder_name = datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
artifact_folder =  os.path.join("artifacts", artifact_folder_name)