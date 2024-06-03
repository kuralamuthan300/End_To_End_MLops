from cgi import test

from flask import Config
from software_defect_prediction.constants import *
from software_defect_prediction.utils.common import read_yaml, create_directories
from software_defect_prediction.entity.config_entity import (DataIngestionConfig, DataTransformationConfig, DataValidationConfig, ModelEvaluationConfig, ModelTrainerConfig, PredictionConfig)

from box import ConfigBox

class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH,
        schema_filepath = SCHEMA_FILE_PATH,
        credentials_filepath = CREDENTIALS_FILE_PATH):
        
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)
        self.__credentials = read_yaml(credentials_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_schema(self) -> ConfigBox:
        return(self.schema)

    def get_model_params(self) -> ConfigBox:
        return(self.params)

    def get_mlflow_credentials(self) -> ConfigBox:
        return(self.__credentials.mlflow)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            source_URL_file_name = config.source_URL_file_name,
            source_URL_unzip_file_name = config.source_URL_unzip_file_name,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir 
        )

        return data_ingestion_config

    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation
        
        create_directories([config.root_dir])
        data_validation_config = DataValidationConfig(
            root_dir = config.root_dir,
            input_file_name = config.input_file_name,
            source_file_path = config.source_file_path,
            STATUS_FILE = config.STATUS_FILE
        )
        return data_validation_config
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation
        
        create_directories([config.root_dir])
        data_transformation_config = DataTransformationConfig(
            root_dir = config.root_dir,
            source_file_path = config.source_file_path,
            input_file_name = config.input_file_name
            
        )
        return data_transformation_config
    
    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer
        
        create_directories([config.root_dir])
        model_trainer_config = ModelTrainerConfig(
            root_dir = config.root_dir,
            source_file_path = config.source_file_path,
            train_file = config.train_file,
            test_file = config.test_file
        )
        
        return(model_trainer_config)

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config = self.config.model_evaluation
        
        create_directories([config.root_dir])
        model_evaluation_config = ModelEvaluationConfig(
            root_dir = config.root_dir,
            source_file_path = config.source_file_path,
            model_file  = config.model_file,
            train_file = config.train_file,
            test_file  = config.test_file,
            perf_metrics_file = config.perf_metrics_file
        )
        
        return(model_evaluation_config)
    
    def get_prediction_config(self) -> PredictionConfig
        config = self.config.prediction
    
        prediction_config = PredictionConfig(
        scaler_obj_path = config.scaler_obj_path
        model_obj_path = config.model_obj_path
        )
        
        return(prediction_config)
    