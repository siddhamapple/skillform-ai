# src/utils/logging_config.py

import logging
import os
from datetime import datetime

def setup_logging():
    logs_path = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_path, exist_ok=True)
    log_file = f'{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.log'
    log_file_path = os.path.join(logs_path, log_file)
    logging.basicConfig(
        filename=log_file_path,
        format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    logging.info("Logging has started")


'''
from utils.logging_config import setup_logging
setup_logging()

'''