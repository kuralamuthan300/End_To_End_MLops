from software_defect_prediction.entity.config_entity import DataIngestionConfig
from software_defect_prediction.config.configuration import ConfigurationManager
import software_defect_prediction.utils
import software_defect_prediction.config

import urllib.request
from pathlib import Path
import zipfile


class data_ingestion():
    def __init__(self,data_ingestion_config : DataIngestionConfig) -> None:
        config = data_ingestion_config
    
    def download_file(self):
        url = self.source_URL
        save_path = Path(self.root_dir,self.source_URL_file_name)
        try:
        # Open a connection to the URL
            with urllib.request.urlopen(url) as response:
            # Read data from the response
                data = response.read()
            
            # Write the data to a file at the specified save path
            with open(save_path, 'wb') as file:
                file.write(data)
                
            logger.info(f"File downloaded successfully to: {save_path}")
        except Exception as e:
            logger.error(f"Failed to download file from {url}: {e}")
            
    def unzip_file(zip_file_path, extract_dir):
        try:
            # Create the extraction directory if it doesn't exist
            os.makedirs(extract_dir, exist_ok=True)

            # Open the zip file for reading
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                # Extract all contents of the zip file to the extraction directory
                zip_ref.extractall(extract_dir)

            logger.info(f"Successfully extracted {zip_file_path} to {extract_dir}")
        except Exception as e:
            logger.error(f"Failed to unzip {zip_file_path}: {e}")