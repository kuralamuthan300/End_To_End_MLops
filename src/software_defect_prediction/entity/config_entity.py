import array
from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import true
from software_defect_prediction import logger

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    source_URL_file_name : str
    source_URL_unzip_file_name : str
    local_data_file: Path
    unzip_dir: Path
    
@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    source_file_path : str
    input_file_name : str
    STATUS_FILE: str 
    
@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    source_file_path : str
    input_file_name : str
    
@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir : Path
    source_file_path : str
    train_file : str
    test_file : str
    
@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir : Path
    source_file_path : str
    model_file : str
    train_file : str
    test_file : str
    perf_metrics_file : str