
from pathlib import Path
from software_defect_prediction.entity.config_entity import PredictionConfig
import joblib

class Prediction :
    def __init__(self, prediction_config : PredictionConfig) -> None:
        self.config = prediction_config
        self.scaler = joblib.load(Path(prediction_config.scaler_obj_path))
        self.model = joblib.load(Path(prediction_config.model_obj_path))
    
    def predict(self,X):
        X_trans = self.scaler.transform(X)
        y_pred = self.model.predict(X_trans)
        return y_pred