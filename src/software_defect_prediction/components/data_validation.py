from software_defect_prediction.entity.config_entity import DataValidationConfig
from software_defect_prediction import logger

import os
from box import ConfigBox
from sys import exception
from pathlib import Path
import shutil
import pandas as pd

class Data_Validation():
    def __init__(self,data_validation_config : DataValidationConfig, data_schema : ConfigBox) -> None:
        self.config = data_validation_config
        self.data_schema = data_schema
        self.VALIDATION_STATUS = False
        
    def prepare_files(self) -> None:
        
        destination_file_path = Path(Path(self.config.root_dir) / Path(self.config.input_file_name))
        if os.path.exists(destination_file_path):
            os.remove(destination_file_path)
        
        shutil.copy(self.config.source_file_path,self.config.root_dir)

    def validate_all_columns(self) -> bool:
        try :
            input_data = pd.read_csv(Path(self.config.root_dir) / Path(self.config.input_file_name))

            input_data_schema = pd.DataFrame({
                "column" : input_data.columns,
                "data_type" : input_data.dtypes
            }).reset_index(drop=True)

            # input_data_schema = input_data_schema[~ input_data_schema["column"].isin(["id","b"])]

            original_data_schema = pd.DataFrame({
                "column" : self.data_schema.COLUMNS.keys(),
                "data_type" : self.data_schema.COLUMNS.values()

            }).reset_index(drop=True)

            # Merge the two DataFrames on both column names and data types
            merged_df = input_data_schema.astype(str).merge(original_data_schema.astype(str), on=['column', 'data_type'], how='outer', indicator=True)

            # Filter rows where the merge indicator is not 'right_only' (i.e., where there is a mismatch with original data schema)
            mismatched_columns = merged_df[merged_df['_merge'] == 'right_only']

            # Print columns causing the mismatch
            if not mismatched_columns.empty:
                logger.error("Columns causing the mismatch: ",str(mismatched_columns['column'].unique()))
                self.VALIDATION_STATUS = False
                with open(self.config.STATUS_FILE, 'w') as f:
                            f.write(f"Validation status: {self.VALIDATION_STATUS}")
            else:
                logger.info("Columns and data types match between the two DataFrames")
                self.VALIDATION_STATUS = True
                with open(self.config.STATUS_FILE, 'w') as f:
                            f.write(f"Validation status: {self.VALIDATION_STATUS}")
                            
            return self.VALIDATION_STATUS
        except exception as e:
            raise e
