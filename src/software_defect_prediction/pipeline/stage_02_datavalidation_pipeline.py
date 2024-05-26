from sys import exception
from software_defect_prediction import logger
from software_defect_prediction.components.data_validation import Data_Validation
from software_defect_prediction.config.configuration import ConfigurationManager

class DataValidationPipeline:
    def __init__(self) -> None:
        pass
    
    def main(self) -> None:
        try:
            configuration_obj = ConfigurationManager()
            data_validation_conf =  configuration_obj.get_data_validation_config()
            data_schema = configuration_obj.get_data_schema()
            
            step_data_val = Data_Validation(data_validation_config=data_validation_conf,data_schema = data_schema)
            logger.info(">>>>>> Data validation run started <<<<<<")
            step_data_val.prepare_files()
            step_data_val.validate_all_columns()
            logger.success(">>>>>> Data validation completed successfully <<<<<<")
        except exception as e:
            logger.error(">>>>>> Data validation failed <<<<<<")
            logger.info(e)