# This script is responsible for extracting the required data
import sklearn
import pandas as pd
import numpy as np
import sklearn.datasets
from src.logger import logger
from src.utils.common import read_yaml
from src.constants import CONFIG_PATH
def get_date():
    logger.info("Data Extraction Started...")
    try:
        data=sklearn.datasets.fetch_california_housing()
        df_data=pd.DataFrame(data.data,columns=data.feature_names)
        df_target=pd.DataFrame(data.target,columns=['price'])
        df=pd.concat([df_data,df_target],axis=1)
        logger.info("Data Extracted Successfully!")
        pathvalue=read_yaml(CONFIG_PATH)
        df.to_csv(pathvalue.data.raw+"/housing_raw_data.csv",index=False)
        logger.info("Data Loaded Successfully!")
    except Exception as e:
        raise e
get_date()