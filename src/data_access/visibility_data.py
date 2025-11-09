from typing import Optional, List
import sys
from pymongo import MongoClient
from database_connect import mongo_operation as mongo
import numpy as np
import pandas as pd
from src.config.mongo_db_connection import MongoDBClient
from src.constant.constant import *
from src.exception import VisibilityException
import os
from dotenv import load_dotenv
load_dotenv()


class Visibility_Data:

    def __init__(self , database_name : str ):
        try:
            self.database_name = database_name
            self.mongo_url = MONGODB_URL
        except Exception as e :
            raise VisibilityException(e , sys)
        
    
    def get_collection_name(self ) -> List :
        mongo_db_client = MongoClient(self.mongo_url)
        collection_names = mongo_db_client[self.database_name]
        return collection_names
    
    def get_collection_data(self , collection_name : str) -> pd.DataFrame :
        mongo_connection = mongo(
            client_url=self.mongo_url,
            database_name=self.database_name,
            collection_name=collection_name
        )
        df = mongo_connection.find()

        if "_id" in df.columns.to_list():
            df = df.drop(columns = '_id')
        
        df = df.replace({"na " : np.nan})
        return df
    

    def export_collection_as_dataframe(self ) -> pd.DataFrame:
        try: 
            collection = self.get_collection_name()

            for collection_name in collection :
                df =self.get_collection_data(collection_name = collection_name)
                yield collection_name , df


        except Exception as e :
            raise VisibilityException(e ,sys)



