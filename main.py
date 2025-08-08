from src.logger import logger
from src.pipelines import extract_data
from src.pipelines import preprocess
from src.pipelines import train

# # Starting the data extraction
# logger.info("----------------------- Starting the run for Data Extraction--------------------------")
# extract_data.get_data()
# Ask user if data extraction should be run
run_extraction = input("❓ Do you want to run the data extraction phase? (yes/no): ").strip().lower()

if run_extraction in ["yes", "y"]:
    logger.info("----------------------- Starting the run for Data Extraction --------------------------")
    extract_data.get_data()
    logger.info("------------------------ Data Extraction pipeline ended -------------------------------")
else:
    logger.info("⚠️  Skipping data extraction phase as per user input.")

# Starting the data preprocessing
logger.info("------------------------------- Starting the run for Data Preprocessing-----------------")
preprocess.run()
logger.info("---------------------------- Data Preprocessing run ended ----------------------------")
# Begginning the training
logger.info("------------------------- Training started----------------------------------------")
train.train_run()
logger.info("------------------------------ Training completed-----------------------------------")