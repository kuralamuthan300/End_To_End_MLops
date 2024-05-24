from software_defect_prediction.config.configuration import ConfigurationManager
from software_defect_prediction.components.data_ingestion import Data_Ingestion
from software_defect_prediction import logger

configuration_obj = ConfigurationManager()
data_ingestion_conf =  configuration_obj.get_data_ingestion_config()
step_data_ing = Data_Ingestion(data_ingestion_conf)
step_data_ing.download_file()
step_data_ing.unzip_file()
logger.success("Data ingestion completed successfully")
