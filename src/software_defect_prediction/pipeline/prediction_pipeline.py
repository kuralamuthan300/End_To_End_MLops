
from pathlib import Path

from numpy import float64
from software_defect_prediction.entity.config_entity import PredictionConfig
import joblib,pandas as pd

class Prediction :
    def __init__(self, prediction_config : PredictionConfig) -> None:
        self.config = prediction_config
        self.scaler = joblib.load(Path(prediction_config.scaler_obj_path))
        self.model = joblib.load(Path(prediction_config.model_obj_path))
    
    def predict(self,X):
        X_trans = self.scaler.transform(X)
        X_trans = pd.DataFrame(X_trans,columns= X.columns)
        X_trans[X_trans.columns] = X_trans[X_trans.columns].astype(float64)
        
        y_pred = self.model.predict(X_trans)
        return y_pred