import psycopg2
from psycopg2 import sql
from datetime import datetime
import json
import os


#Read secrets only if not running in CI
if os.getenv("CI_ENV")!="true":
    from src.constants import SECRET_PATH
    from src.utils.common import read_yaml
    DB_CONNECT=read_yaml(SECRET_PATH)
    # Database connection parameters (you can also load from a config file or env vars)
    DB_PARAMS = {
        "dbname": DB_CONNECT['PostGres_DB']['DB_NAME'] ,
        "user": DB_CONNECT['PostGres_DB']['DB_USER'],
        "password": DB_CONNECT['PostGres_DB']['DB_PWD'],
        "host": DB_CONNECT['PostGres_DB']['DB_HOST'],
        "port": DB_CONNECT['PostGres_DB']['DB_PORT']
    }
else:
    DB_CONNECT=None



def init_db():
    if(os.getenv("CI_ENV")=="true"):
        print("Running in CI - Skipping DB Init")
        return
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id SERIAL PRIMARY KEY,
            input JSONB,
            output REAL,
            timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def log_to_db(input_data: dict, prediction: float):
    if(os.getenv("CI_ENV")=="true"):
        print("Running in CI - skipping DB logging")
        return
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO predictions (input, output) VALUES (%s, %s)
    """, (json.dumps(input_data), prediction))
    conn.commit()
    conn.close()
