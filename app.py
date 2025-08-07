from fastapi import FastAPI
from pydantic import BaseModel,Field
from typing import Annotated
import joblib
import numpy as np
import pandas as pd
from src.utils.common import read_yaml
from src.constants import CONFIG_PATH
from pathlib import Path
import json
#from src.utils.log_db import init_db,log_to_db


#read the Config path
path=read_yaml(CONFIG_PATH)

#Load the model
model=joblib.load(Path(path['models']['model_path'])/'best_model.pkl')

#Load the scalar model
scaler=joblib.load(Path(path['models']['model_path'])/'scaler.pkl')

#Load the pop_99 
pop_99 = joblib.load(Path(path['models']['model_path'])/'pop_99.pkl')

#definition for preprocess function
def preprocess_input(df: pd.DataFrame) -> pd.DataFrame:
    # 1. Log transform
    df['MedInc'] = np.log(df['MedInc'])

    # 2. Apply the same scaler as training
    scaled = scaler.transform(df)
    scaled_df = pd.DataFrame(scaled, columns=df.columns)

    # 3. Clip Population at 99th percentile (based on training data)
    scaled_df['Population'] = scaled_df['Population'].clip(upper=pop_99)

    return scaled_df
  
    

#Input Schema using PyDantic
class InputData(BaseModel):
    MedInc: Annotated[float,Field(...,description="median income in block group")]
    HouseAge: Annotated[float,Field(...,description="median house age in block group")]
    Population: Annotated[float,Field(...,description="block group population")]
    Longitude: Annotated[float,Field(...,description="block group longitude")]
    Latitude: Annotated[float,Field(...,description="block group latitude")]
    

#Initiaing an app
app=FastAPI()

@app.get("/")
def read():
    return {"message":"California Housing Prediction is running..."}

# initiating the connection
#init_db()

@app.post("/predict")
def predict(data:InputData):
    input_df=pd.DataFrame([data.model_dump()])
    #preprocessing the input first before predicting
    input_df=preprocess_input(input_df)
    res=model.predict(input_df)
    #Save to postgres
    #log_to_db(data.model_dump(),float(res[0]))
    return  {"prediction:",float(res[0])} #input_df.to_dict(orient="records")[0]

# uvicorn app:app --reload

    