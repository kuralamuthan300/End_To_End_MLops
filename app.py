from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from software_defect_prediction import logger
from software_defect_prediction.pipeline.prediction_pipeline import Prediction
from software_defect_prediction.config.configuration import ConfigurationManager
import pandas as pd
from subprocess import run

app = FastAPI(
    title="Software Defect Prediction API",
    description="Predict software defects using machine learning models",
    version="1.0.0"
)

class SoftwareDefectPredictionData(BaseModel):
    """
    Data structure for software defect prediction input.
    """
    loc: float  # Lines of code
    v_g: float  # McCabe's cyclomatic complexity for decision statements
    ev_g: float  # McCabe's cyclomatic complexity for executable statements
    iv_g: float  # McCabe's cyclomatic complexity for predicate statements
    n: float  # Halstead's deliverable lines
    v: float  # Halstead's volume
    l: float  # Halstead's difficulty
    d: float  # Halstead's programming effort
    i: float  # Halstead's programming time
    e: float  # Halstead's bugs
    b: float  # Halstead's delivered bugs
    t: float  # Halstead's potential bugs
    lOCode: int  # Lines of code excluding comments
    lOComment: int  # Lines of comments
    lOBlank: int  # Lines of blank code
    locCodeAndComment: int  # Lines of code and comments combined
    uniq_Op: float  # Number of unique operators
    uniq_Opnd: float  # Number of unique operands
    total_Op: float  # Total number of operators
    total_Opnd: float  # Total number of operands
    branchCount: float  # Number of branches in the code

@app.get("/")
async def root():
    """
    Returns a welcome message for the API.
    """
    return {"message": "Welcome to the Software Defect Prediction API!"}

@app.post("/train/", response_model=str)
async def train():
    """
    Initiates the training process for the software defect prediction model.

    This endpoint does not directly execute arbitrary Python code for security reasons.
    It assumes the existence of a separate training script (`main.py`) that can be
    invoked safely.

    Raises:
        HTTPException: If the training process encounters an error.
    """

    try:
        # Use subprocess with appropriate arguments to control execution
        training_process = run(["python", "main.py"], capture_output=True)
        training_output = training_process.stdout.decode("utf-8")
        logger.info(f"training completed: {training_output}")
        return "training completed successfully."
    except Exception as e:
        logger.error(f"training failed: {e}")
        raise HTTPException(status_code=500, detail="training failed.")
    
@app.post("/predict/", response_model=list[float])
async def predict(params: SoftwareDefectPredictionData):
    """
    Predicts software defects using a machine learning model.

    Args:
        data (SoftwareDefectPredictionData): Input data for prediction.

    Returns:
        list[float]: List of predicted defect probabilities.
    """
    try:
        config_manager = ConfigurationManager()
        prediction_pipeline = Prediction(config_manager.get_prediction_config())

        data_list = [params]
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

        y_pred = prediction_pipeline.predict(df)
        return y_pred.tolist() if hasattr(y_pred, 'tolist') else y_pred
    except Exception as e:
        return {"error": str(e)}  # Handle exceptions and return informative error message