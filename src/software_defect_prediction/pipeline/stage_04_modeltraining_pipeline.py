from sys import exception
from software_defect_prediction import logger
from software_defect_prediction.components.model_trainer import Model_Trainer, ModelTrainerConfig
from software_defect_prediction.config.configuration import ConfigurationManager

class ModelTrainingPipeline:
    def __init__(self) -> None:
        pass
    
    def main(self) -> None:
        try:
            configuration_obj = ConfigurationManager()
            modeltrainer_obj = configuration_obj.get_model_trainer_config()
            data_schema = configuration_obj.get_data_schema()
            predictor = data_schema.TARGET_COLUMN.name
            model_params = configuration_obj.get_model_params()
            
            step_model_train = Model_Trainer(modeltrainer_obj,model_params,predictor)
            logger.info(">>>>>> Model Training started <<<<<<")
            step_model_train.prepare_and_load_files()
            step_model_train.train_model()
            logger.success(">>>>>> Model Training completed successfully <<<<<<")
            
        except exception as e:
            logger.error(">>>>>> Model Training failed <<<<<<")
            logger.info(e)