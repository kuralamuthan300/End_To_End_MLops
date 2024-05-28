from sys import exception
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from software_defect_prediction.config.configuration import DataTransformationConfig
import shutil
from pathlib import Path
import os
from software_defect_prediction import logger
import joblib

class Data_Transformation():
    def __init__(self,data_transformation_config : DataTransformationConfig, predictor_col : str) -> None:
        self.config = data_transformation_config
        self.predictor_col = predictor_col
        self.input_df = None
        
    def prepare_and_load_files(self) -> None:
        try :
            destination_file_path = Path(Path(self.config.root_dir) / Path(self.config.input_file_name))
            if os.path.exists(destination_file_path):
                os.remove(destination_file_path)
        
            shutil.copy(self.config.source_file_path,self.config.root_dir)
            
            input_file_path = Path(Path(self.config.root_dir) / Path(self.config.input_file_name))
            self.input_df = pd.read_csv(input_file_path)
            
            logger.info("input file loaded successfully")
        except exception as e:
            logger.error("input file loading failed")
            raise(e)
        
    def tr_test_split_and_transform(self) -> None:
        try :
            input_df = self.input_df
            predictor_col = self.predictor_col
            X = input_df.drop(columns=[predictor_col])
            y = input_df[predictor_col]
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42, stratify=y, shuffle=True)
            logger.info("train test split completed")

            robust_scaler = RobustScaler().fit(X_train.drop(columns="id"))

            X_train_scaled = pd.DataFrame(robust_scaler.transform(X_train.drop(columns="id")), columns=X_train.columns.drop('id'))
            X_test_scaled = pd.DataFrame(robust_scaler.transform(X_test.drop(columns="id")), columns=X_test.columns.drop('id'))

            X_train_scaled['id'] = X_train['id'].values
            X_test_scaled['id'] = X_test['id'].values

            train_df = pd.concat([X_train_scaled, y_train.reset_index(drop=True)], axis=1)
            test_df = pd.concat([X_test_scaled, y_test.reset_index(drop=True)], axis=1)

            logger.info("train and test data scaling through robust scaler completed")
            
            joblib.dump(robust_scaler,Path(self.config.root_dir/Path("robust_scaler.joblib")))
            train_df.to_csv(Path(self.config.root_dir/Path("train_data.csv")), index=False)
            test_df.to_csv(Path(self.config.root_dir/Path("test_data.csv")), index=False)
            
            logger.info(f"robust_scaler.joblib, train_data.csv, test_data.csv are saved to ",Path(self.config.root_dir/Path("train_data.csv")))

        except exception as e :
            raise(e)