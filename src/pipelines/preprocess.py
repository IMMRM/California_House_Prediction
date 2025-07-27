import sklearn as sk
import numpy as np
import pandas as pd
import yaml
from src.logger import logger
from src.constants import CONFIG_PATH
from src.utils.common import read_yaml
from pathlib import Path
from sklearn.preprocessing import StandardScaler
import joblib as jb


#reading the parameters of configuration file here
params=read_yaml(CONFIG_PATH)

#preprocess pipeline function
def preprocess(input_path,output_path):
    try:
        df=pd.read_csv(input_path)
        df['MedInc']=np.log(df['MedInc'])
        #important features
        features=['MedInc','HouseAge','Population','Longitude','Latitude','price']
        df=df[features]
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(df.drop('price', axis=1))
        scaled_df = pd.DataFrame(scaled_features, columns=df.columns[:-1])
        # Clip outliers (e.g., cap at 99th percentile)
        for col in ['Population']:
            upper_limit = scaled_df[col].quantile(0.99)
            scaled_df[col] = scaled_df[col].clip(upper=upper_limit)
        scaled_df=pd.concat([scaled_df,df['price']],axis=1)
        scaled_df.to_csv(output_path,index=False)
        logger.info(" Data Preprocessing was successfull!")
        return scaler
    except Exception as e:
        logger.error(e)

#function responsible for the run
def run():
    scaler=preprocess(Path(params['data']['raw'])/"housing_raw_data.csv",Path(params['data']['processed'])/"processed_data.csv")
    jb.dump(scaler,Path(params['models']['model_path'])/"scaler.pkl")
    
