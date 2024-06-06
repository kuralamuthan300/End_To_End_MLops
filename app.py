from fastapi import FastAPI
from pydantic import BaseModel
from software_defect_prediction.pipeline.prediction_pipeline import Prediction
from software_defect_prediction.config.configuration import ConfigurationManager
import pandas as pd

app = FastAPI()

class SoftwareDefectPredictionData(BaseModel):
  loc : float
  v_g : float
  ev_g : float
  iv_g : float
  n : float
  v : float
  l : float
  d : float
  i : float
  e : float
  b : float
  t : float
  lOCode : int
  lOComment : int
  lOBlank : int
  locCodeAndComment : int
  uniq_Op : float
  uniq_Opnd : float
  total_Op : float
  total_Opnd : float
  branchCount : float

@app.get("/")
async def home():
    return {"message": "Hello!"}

@app.post("/predict/")
async def predict(X : SoftwareDefectPredictionData):
    config_manager = ConfigurationManager()
    prediction_obj = Prediction(config_manager.get_prediction_config())
    
    data_list = [X]
    data = []
    for obj in data_list:
        row_data = {
            'loc': obj.loc,
            'v_g': obj.v_g,
            'ev_g': obj.ev_g,
            'iv_g': obj.iv_g,
            'n': obj.n,
            'v': obj.v,
            'l': obj.l,
            'd': obj.d,
            'i': obj.i,
            'e': obj.e,
            'b': obj.b,
            't': obj.t,
            'lOCode': obj.lOCode,
            'lOComment': obj.lOComment,
            'lOBlank': obj.lOBlank,
            'locCodeAndComment': obj.locCodeAndComment,
            'uniq_Op': obj.uniq_Op,
            'uniq_Opnd': obj.uniq_Opnd,
            'total_Op': obj.total_Op,
            'total_Opnd': obj.total_Opnd,
            'branchCount': obj.branchCount
        }
        data.append(row_data)

    df = pd.DataFrame(data)
    df.rename(columns={'v_g': 'v(g)', 'ev_g': 'ev(g)', 'iv_g': 'iv(g)'}, inplace=True)
    
    y_pred = prediction_obj.predict(df)
    return {"prediction": y_pred.tolist() if hasattr(y_pred, 'tolist') else y_pred}