from sys import exception
from software_defect_prediction import logger
from software_defect_prediction.components.data_transformation import Data_Transformation
from software_defect_prediction.config.configuration import ConfigurationManager

class DataTransformationPipeline:
    def __init__(self) -> None:
        pass
    
    def main(self) -> None:
        try:
            configuration_obj = ConfigurationManager()
            data_transformation_conf = configuration_obj.get_data_transformation_config()
            data_schema = configuration_obj.get_data_schema()
            predictor = data_schema.TARGET_COLUMN.name
            
            step_data_trans = Data_Transformation(data_transformation_conf,predictor)
            logger.info(">>>>>> Data transformation started <<<<<<")
            step_data_trans.prepare_and_load_files()
            step_data_trans.tr_test_split_and_transform()
            logger.success(">>>>>> Data transformation completed successfully <<<<<<")
            
        except exception as e:
            logger.error(">>>>>> Data transformation failed <<<<<<")
            logger.info(e)