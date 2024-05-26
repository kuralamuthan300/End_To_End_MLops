from software_defect_prediction import logger
from software_defect_prediction.pipeline.stage_01_dataingestion_pipeline import DataIngestionPipeline

logger.info(">>>>>> Data ingestion run started <<<<<<")
dataingestion_pipeline = DataIngestionPipeline()
dataingestion_pipeline.main()
logger.info(">>>>>> Data ingestion run finished <<<<<<")