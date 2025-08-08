import pandas as pd
import psycopg2
from datetime import datetime
import subprocess
import os
from src.utils.common import read_yaml
from src.constants import CONFIG_PATH, SECRET_PATH
from src.pipelines import preprocess
from pathlib import Path
from src.logger import logger

# Load secrets and config
config = read_yaml(CONFIG_PATH)
secrets = read_yaml(SECRET_PATH)

DB_PARAMS = {
    "dbname": secrets['PostGres_DB']['DB_NAME'],
    "user": secrets['PostGres_DB']['DB_USER'],
    "password": secrets['PostGres_DB']['DB_PWD'],
    "host": secrets['PostGres_DB']['DB_HOST'],
    "port": secrets['PostGres_DB']['DB_PORT']
}

def fetch_new_data():
    conn = psycopg2.connect(**DB_PARAMS)
    df = pd.read_sql("SELECT * FROM new_housing_data;", conn)
    conn.close()
    return df

def retrain_with_new_data():
    logger.info("------------Fetching data from new source---------------------")
    df = fetch_new_data()
    if df.empty:
        print("No new data found, skipping retrain.")
        return
    # Step 0: preprocess the data
    raw_path = os.path.join(config['data']['raw'], "housing_raw_data.csv")
    df.to_csv(raw_path,index=False)
    print("✅ New Data saved to raw path")
    print("-----Starting preprocessing-----")
    preprocess.run()
    print("---preprocessing completed--------")
    # Step 1: Overwrite processed_data.csv
    processed_path = os.path.join(config['data']['processed'], "processed_data.csv")
    print(f"Overwrote: {processed_path}")

    # Step 2: Call train.py via subprocess
    print("⏳ Retraining model...")
    logger.info("-------Starting retraining-------------------")
    
    # 👇 Absolute path to train.py
    train_script_path = Path(__file__).resolve().parent.parent.parent / "main.py"

    # 👇 Just run it without setting cwd now
    subprocess.run(["python", str(train_script_path)], check=True)
    print("✅ Retraining complete via train.py")
    logger.info("--------------------Retraining Ended---------------------------")


if __name__ == "__main__":
    retrain_with_new_data()
