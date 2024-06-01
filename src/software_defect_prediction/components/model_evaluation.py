from sys import exception
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    matthews_corrcoef,
    cohen_kappa_score,
    balanced_accuracy_score,
    hamming_loss,
    jaccard_score,
)
from pathlib import Path
import os
import shutil
import json
from mlflow.models import infer_signature
import mlflow
import joblib
from box import ConfigBox

from software_defect_prediction import *
from software_defect_prediction.config.configuration import ModelEvaluationConfig


class Model_Evaulation():
    def __init__(
        self,
        model_evaluation_config : ModelEvaluationConfig, 
        model_parameters : dict ,
        predictor_col : str,
        mlflow_tracking : ConfigBox) -> None:
        self.config = model_evaluation_config
        self.predictor_col = predictor_col
        self.model_parameters = model_parameters.MODEL_PARAMETERS.to_dict()
        self.__mlflow_tracking = mlflow_tracking
        self.model = None
        self.train_df = None
        self.test_df = None
        
    def prepare_and_load_files(self) -> None:
        try :
            
            files_arr = [self.config.train_file,self.config.test_file,self.config.model_file]
            
            for file_name in files_arr:
                source_file_path = Path(Path(self.config.source_file_path) / Path(file_name))
                destination_file_path = Path(Path(self.config.root_dir) / Path(file_name))
                if os.path.exists(destination_file_path):
                    os.remove(destination_file_path)

                shutil.copy(source_file_path,self.config.root_dir)
            logger.info(Path(self.config.root_dir) / Path(self.config.train_file))
            self.train_df = pd.read_csv(Path(self.config.root_dir) / Path(self.config.train_file))
            self.test_df = pd.read_csv(Path(self.config.root_dir) / Path(self.config.test_file))
            self.model = joblib.load(Path(Path(self.config.root_dir) / Path("random_forest_model.joblib")))
            logger.info("model, train and test data loaded successfully")
            
        except exception as e:
            logger.error("model, train and test data loding failed")
            raise(e)
    
    def setup_mlflow(self) -> None:
        os.environ['MLFLOW_TRACKING_URI'] = self.__mlflow_tracking.MLFLOW_TRACKING_URI
        os.environ['MLFLOW_TRACKING_USERNAME'] =  self.__mlflow_tracking.MLFLOW_TRACKING_USERNAME
        os.environ['MLFLOW_TRACKING_PASSWORD'] = self.__mlflow_tracking.MLFLOW_TRACKING_PASSWORD
    
    def eval_metrics_classification(self, actual, pred) -> None:
        accuracy = accuracy_score(actual, pred)
        precision = precision_score(actual, pred, average='weighted')
        recall = recall_score(actual, pred, average='weighted')
        f1 = f1_score(actual, pred, average='weighted')
        roc_auc = roc_auc_score(actual, pred, average='weighted', multi_class='ovr')
        # cm = confusion_matrix(actual, pred)
        mcc = matthews_corrcoef(actual, pred)
        cohen_kappa = cohen_kappa_score(actual, pred)
        balanced_acc = balanced_accuracy_score(actual, pred)
        hamming = hamming_loss(actual, pred)
        jaccard = jaccard_score(actual, pred, average='weighted')
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'roc_auc': roc_auc,
            # 'confusion_matrix': cm,
            'mcc': mcc,
            'cohen_kappa': cohen_kappa,
            'balanced_accuracy': balanced_acc,
            'hamming_loss': hamming,
            'jaccard_score': jaccard
        }
        
    def log_into_mlflow(self) -> None:
        
        X_train = self.train_df.drop(columns=['id',self.predictor_col])
        
        X_test = self.test_df.drop(columns=['id',self.predictor_col])
        y_test = self.test_df[self.predictor_col].astype(int)
        
        mlflow.set_tracking_uri(uri=self.__mlflow_tracking.MLFLOW_TRACKING_URI)
        mlflow.set_experiment(self.__mlflow_tracking.MLFLOW_TRACKING_EXPERIMENT)
        
        with mlflow.start_run():
            
            y_pred = self.model.predict(X_test)
            
            model_perf_metrics = self.eval_metrics_classification(actual=y_test,pred=y_pred)
            with open(Path(Path(self.config.root_dir) / Path(self.config.perf_metrics_file)), "w") as outfile: 
                json.dump(model_perf_metrics, outfile)
            
            mlflow.log_params(self.model_parameters)
            for metric_name, value in model_perf_metrics.items():
                mlflow.log_metric(metric_name, value)

            signature = infer_signature(X_train, self.model.predict(X_train))

            mlflow.sklearn.log_model(
                sk_model=self.model,
                signature=signature,
                input_example=X_train,
                artifact_path="software_defect_prediction",
                registered_model_name="RandomForestClassifier",
            )