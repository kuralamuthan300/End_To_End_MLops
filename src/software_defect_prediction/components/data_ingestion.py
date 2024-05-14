import software_defect_prediction.utils
import software_defect_prediction.config

class data_ingestion():
    def __init__(self,data_ingestion_config : DataIngestionConfig) -> None:
        config = data_ingestion_config
    
    def download_dataset(self) -> None:
        pass