from software_defect_prediction.config.configuration import ModelTrainerConfig
from software_defect_prediction import *

import joblib
import shutil
import pandas as pd
from pathlib import Path
from sys import exception
from sklearn.ensemble import RandomForestClassifier



class Model_Trainer():
    def __init__(self,model_trainer_config : ModelTrainerConfig, model_parameters : dict ,predictor_col : str) -> None:
        self.config = model_trainer_config
        self.predictor_col = predictor_col
        self.model_parameters = model_parameters.MODEL_PARAMETERS.to_dict()
        self.train_df = None
        
    def prepare_and_load_files(self) -> None:
        try :
            
            files_arr = [self.config.train_file,self.config.test_file]
            
            for file_name in files_arr:
                source_file_path = Path(Path(self.config.source_file_path) / Path(file_name))
                destination_file_path = Path(Path(self.config.root_dir) / Path(file_name))
                if os.path.exists(destination_file_path):
                    os.remove(destination_file_path)

                shutil.copy(source_file_path,self.config.root_dir)

            self.train_df = pd.read_csv(Path(Path(self.config.root_dir) / Path(self.config.train_file)))
            logger.info("input file loaded successfully")
            
        except exception as e:
            logger.error("input file loading failed")
            raise(e)
        
    def train_model(self) -> None:
        try :
            X_train = self.train_df.drop(columns=['id','defects'])
            y_train = self.train_df.defects.astype(int)
            logger.info("model training started")
            rf_clf = RandomForestClassifier(**self.model_parameters,random_state=42)
            rf_clf.fit(X_train,y_train)
            
            model_savepath = Path(self.config.root_dir)/Path("random_forest_model.joblib")
            
            joblib.dump(rf_clf, model_savepath)
            logger.info(f"model training completed and model file saved to {model_savepath}")
        except exception as e:
            logger.error("model training failed")
            raise(e)
            
                
