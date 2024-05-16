from dataclasses import dataclass
from pathlib import Path
from software_defect_prediction import logger

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    source_URL_file_name : str
    source_URL_unzip_file_name : str
    local_data_file: Path
    unzip_dir: Path