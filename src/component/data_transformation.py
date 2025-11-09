import sys
from typing import Union
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from src.component.ingestion import DataIngestion

from collections import namedtuple
from src.constant.constant import *
from src.exception import VisibilityException
from src.logger import logging
from src.utils.utils import MainUtils
from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
    data_transformation_dir: str = os.path.join(artifact_folder, "data_transformation")
    train_transformed_file_path: str = os.path.join(data_transformation_dir, "train.csv")
    test_transformed_file_path : str = os.path.join(data_transformation_dir, "test.csv")


class DataTransformation:
    def __init__(self ):
        self.data_transformation_config = DataTransformationConfig()
        self.utils =  MainUtils()
        
    


    def drop_schema_columns(self , dataframe : pd.DataFrame) -> pd.DataFrame:
        try : 
            _schema_config = self.utils.read_schema_config_file()
            df = dataframe.drop(columns=_schema_config['drop_columns'])
            return df
        except Exception as e:
            raise VisibilityException(e)
    
    @staticmethod
    def get_merged_batch_data(valid_data_dir:str) -> pd.DataFrame:
        try:
            raw_files = os.listdir(valid_data_dir)
            csv_data = []
            for filename in raw_files:
                data = pd.read_csv(os.path.join(valid_data_dir , filename))
                csv_data.append(data)

            merged_data = pd.concat(csv_data)

            return merged_data
        except Exception as e:
            raise VisibilityException(e)
        
    



    def initiate_data_transformation(self):
        logging.info("Entered initiate_data_transformation method of Data_Transformation class"
       )
        try:
            data_ingestion=DataIngestion()



            dataframe = data_ingestion.get_data_ingestion()
            dataframe = self.drop_schema_columns(dataframe =dataframe)

            X = dataframe.drop(columns=TARGET_COLUMN)
            y = dataframe[TARGET_COLUMN]

            X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.2 )

            preprocessor = StandardScaler()

            X_train_scaled =  preprocessor.fit_transform(X_train)
            X_test_scaled  =  preprocessor.transform(X_test)

            preprocessor_path = self.data_transformation_config.data_transformation_dir
            os.makedirs(preprocessor_path, exist_ok=True)
            self.utils.save_object(os.path.join(preprocessor_path , 'preprocessor.pkl') ,preprocessor)

            train_arr = np.c_[X_train_scaled, np.array(y_train)]
            test_arr  = np.c_[X_test_scaled, np.array(y_test)]
            train_arr = pd.DataFrame(train_arr)
            test_arr = pd.DataFrame(test_arr)
            train_arr.to_csv(self.data_transformation_config.train_transformed_file_path)
            test_arr.to_csv(self.data_transformation_config.test_transformed_file_path)

            return (train_arr , test_arr , preprocessor_path)
        except Exception as e:
            raise VisibilityException(e)

if __name__ == "__main__":
    obj = DataTransformation()
    obj.initiate_data_transformation()

            









        


    