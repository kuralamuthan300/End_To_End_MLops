from sys import exception
from software_defect_prediction import logger
from software_defect_prediction.components.model_evaluation import Model_Evaulation, ModelEvaluationConfig
from software_defect_prediction.config.configuration import ConfigurationManager

class ModelEvaluationPipeline:
    def __init__(self) -> None:
        pass
    
    def main(self) -> None:
        try:
            configuration_obj = ConfigurationManager()
            modeleval_obj = configuration_obj.get_model_evaluation_config()
            model_params = configuration_obj.get_model_params()
            predictor = configuration_obj.get_data_schema().TARGET_COLUMN.name

            model_eval = Model_Evaulation(modeleval_obj,model_params,predictor,configuration_obj.get_mlflow_credentials())

            logger.info(">>>>>> Model Evaluation started <<<<<<")
            model_eval.prepare_and_load_files()
            model_eval.setup_mlflow()
            model_eval.log_into_mlflow()
            logger.success(">>>>>> Model Evaluation completed successfully <<<<<<")
            
        except exception as e:
            logger.error(">>>>>> Model Evaluation failed <<<<<<")
            logger.info(e)