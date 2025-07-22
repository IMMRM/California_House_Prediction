# This is the logger file
import os
import sys
import logging
from datetime import datetime

logging_str="[%(asctime)s : %(levelname)s : %(module)s : %(message)s]"
log_dir="logs"

log_filepath=os.path.join(log_dir,f"log_{datetime.now().strftime('%Y-%m-%d-%H')}.log")

os.makedirs(log_dir,exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(log_filepath), #this will write log data in filepath mentioned
        logging.StreamHandler(sys.stdout)
    ]
)
logger=logging.getLogger("CustomLogger")