import psycopg2
from psycopg2 import sql
from datetime import datetime
import json
from src.constants import CONFIG_PATH
from src.utils.common import read_yaml

DB_CONNECT=read_yaml(CONFIG_PATH)

# Database connection parameters (you can also load from a config file or env vars)
DB_PARAMS = {
    "dbname": 'postgres', #DB_CONNECT['PostGres_DB']['DB_NAME'] ,
    "user": 'postgres', #DB_CONNECT['PostGres_DB']['DB_USER'],
    "password": 'postgres' ,#DB_CONNECT['PostGres_DB']['DB_PWD'],
    "host": 'database-1.c5eqggq6w2s1.ap-south-1.rds.amazonaws.com', #DB_CONNECT['PostGres_DB']['DB_HOST'],
    "port": 5432
}

def init_db():
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
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO predictions (input, output) VALUES (%s, %s)
    """, (json.dumps(input_data), prediction))
    conn.commit()
    conn.close()
