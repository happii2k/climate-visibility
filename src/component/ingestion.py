import logging
import sys
import pandas as pd
from pymongo import MongoClient
from zipfile import Path
from src.constant import *
from src.constant.constant import *
from src.exception import VisibilityException
from src.logger import logging

from src.data_access.visibility_data import Visibility_Data
from src.utils.utils import MainUtils
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    data_ingestion_dir : str =  os.path.join(artifact_folder , "data_ingestion")


class DataIngestion:
    def __init__ (self) :
        self.data_ingestion_dir = DataIngestionConfig()


    def get_data (self):
        try : 
            logging.info("Getting data from Mongodb")
            data = Visibility_Data(database_name=MONGO_DATABASE_NAME)
            logging.info("Data fetched successfully from Mongodb")
            collection_name = data.get_collection_name()
            logging.info(f"Fetching data from collection: {collection_name}")
            collection_data = data.get_collection_data(collection_name.list_collection_names()[0])
            logging.info(f"Data fetched successfully from collection: {collection_name}")
            return collection_data
        except Exception as e :
            raise VisibilityException(e )
        
    def export_data_into_raw_data_dir(self) -> pd.DataFrame:
        """
        Method Name :   export_data_into_feature_store
        Description :   This method reads data from mongodb and saves it into artifacts. 
        
        Output      :   dataset is returned as a pd.DataFrame
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   0.1
       
        """
        try:
            logging.info("Exporting data from Mongodb to pandas DataFrame")
            raw_file_path = self.data_ingestion_dir.data_ingestion_dir
            logging.info(f"Creating directory at path: {raw_file_path} if it does not exist")
            os.makedirs(raw_file_path, exist_ok=True)
            df = self.get_data()

            data = Visibility_Data(database_name=MONGO_DATABASE_NAME)
     
            feature_store_file_path = os.path.join(raw_file_path, data.get_collection_name()+'.csv')
            df.to_csv(feature_store_file_path,index=False)

            logging.info("Data export successful")
            return df

        except Exception as e:
            raise VisibilityException(e)
        
    def initiate_data_ingestion(self) -> Path:
        """
            Method Name :   initiate_data_ingestion
            Description :   This method initiates the data ingestion components of training pipeline 
            
            Output      :   train set and test set are returned as the artifacts of data ingestion components
            On Failure  :   Write an exception log and then raise an exception
            
            Version     :   1.2
            Revisions   :   moved setup to cloud
        """
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")

        try:
            self.export_data_into_raw_data_dir()

            logging.info("Got the data from mongodb")


            logging.info(
                "Exited initiate_data_ingestion method of Data_Ingestion class"
            )
            
            return self.data_ingestion_config.data_ingestion_dir

        except Exception as e:
            raise VisibilityException(e) 
    
    def get_data_ingestion(self  ) -> pd.DataFrame:
        try:
            data = Visibility_Data(database_name=MONGO_DATABASE_NAME)
            logging.info("Fetching data from Mongodb")
            feature_store_file_path = os.path.join(self.data_ingestion_dir.data_ingestion_dir, data.get_collection_name().list_collection_names()[0]+'.csv')
            logging.info(f"Reading data from path: {feature_store_file_path}")
            df = pd.read_csv(feature_store_file_path)
            return df
        except Exception as e:
            raise VisibilityException(e)
        
        

        

if __name__ == "__main__":
    obj = DataIngestion()
    obj.get_data_ingestion()










