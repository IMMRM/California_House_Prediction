from src.logger import logger
from src.pipelines import extract_data
from src.pipelines import preprocess

# Starting the data extraction
logger.info("----------------------- Starting the run for Data Extraction--------------------------")
extract_data.get_data()
logger.info("------------------------ Data Extraction pipeline ended ----------------------------")
# Starting the data preprocessing
logger.info("------------------------------- Starting the run for Data Preprocessing-----------------")
preprocess.run()
logger.info("---------------------------- Data Preprocessing run ended ----------------------------")