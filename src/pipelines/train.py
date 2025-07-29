import dagshub
#dagshub.init(repo_owner='mehraj.mirdha', repo_name='California_House_Prediction', mlflow=True)

import pandas as pd
import numpy as np
import mlflow
from mlflow.models.signature import infer_signature
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os
from src.constants import CONFIG_PATH,SECRET_PATH
from src.utils.common import read_yaml
from pathlib import Path
from datetime import datetime

params=read_yaml(CONFIG_PATH)
repo_params=read_yaml(SECRET_PATH)
dagshub.init(repo_owner=repo_params['repo_details']['repo_owner'], repo_name=repo_params['repo_details']['repo_name'], mlflow=True)
# 1. Load preprocessed data
df = pd.read_csv(Path(params['data']['processed'])/'processed_data.csv')

def train_run():
    # 2. Split features and price
    X = df.drop("price", axis=1)
    y = df["price"]

    # 3. Train/Test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Start MLflow tracking
    mlflow.set_experiment("California_Housing_Regression")

    def eval_metrics(y_true, y_pred):
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        r2 = r2_score(y_true, y_pred)
        return mae, rmse, r2
    LR_model_name="Linear Regresssion"
    DT_model_name="Decision Tree"
    timestamp=datetime.now().strftime("%Y-%m-%d-%H:%M")
    
    # 5. Model 1: Linear Regression
    with mlflow.start_run(run_name=f"{LR_model_name}_{timestamp}"):
        lr = LinearRegression()
        lr.fit(X_train, y_train)
        preds = lr.predict(X_test)

        mae, rmse, r2 = eval_metrics(y_test, preds)

        mlflow.log_param("model", "LinearRegression")
        mlflow.log_metric("MAE", mae)
        mlflow.log_metric("RMSE", rmse)
        mlflow.log_metric("R2", r2)
        signature=infer_signature(X_train,y_train)
        mlflow.sklearn.log_model(lr, "model",signature=signature)

        print(f"LR - MAE: {mae}, RMSE: {rmse}, R2: {r2}")

    # 6. Model 2: Decision Tree
    with mlflow.start_run(run_name=f"{DT_model_name}_{timestamp}"):
        dt = DecisionTreeRegressor(max_depth=5)
        dt.fit(X_train, y_train)
        preds = dt.predict(X_test)

        mae, rmse, r2 = eval_metrics(y_test, preds)

        mlflow.log_param("model", "DecisionTree")
        mlflow.log_param("max_depth", 5)
        mlflow.log_metric("MAE", mae)
        mlflow.log_metric("RMSE", rmse)
        mlflow.log_metric("R2", r2)
        mlflow.sklearn.log_model(lr, "model",signature=signature)
        mlflow.sklearn.log_model(dt, "model")

        print(f"DT - MAE: {mae}, RMSE: {rmse}, R2: {r2}")

        # Save locally to use in API
        joblib.dump(dt, Path(params['models']['model_path'])/"best_model.pkl")  # DecisionTree is better
