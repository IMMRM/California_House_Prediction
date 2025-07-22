#It is used to store utiliy/common helper functions that are reusable across different modules. This keeps the codebase clean,modular and maintainable by avoiding redundancy.
from ensure import ensure_annotations
from box import ConfigBox
from box.exceptions import BoxValueError
import yaml
from pathlib import Path
from src.logger import logger


@ensure_annotations
def read_yaml(path_to_yaml:Path)->ConfigBox:
    try:
        with open(path_to_yaml,'r') as yaml_file:
            content=yaml.safe_load(yaml_file)
            logger.info(f"Yaml file {yaml_file} loaded successfully!")
            return ConfigBox(content)
    except BoxValueError as e:
        raise ValueError("Yaml file is empty")
    except Exception as e:
        raise e