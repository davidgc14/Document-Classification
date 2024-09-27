import logging
import os
from datetime import datetime


def create_logger(name):
    today = datetime.now().strftime('%Y%m%d')

    log_folder = 'logs'
    log_path = os.path.join(log_folder, f'log_{today}.log')
    short_log_path = os.path.join(log_folder, f'short_log_{today}.log')


    # Create the handlers
    console_handler = logging.StreamHandler()
    short_handler = logging.FileHandler(short_log_path)
    file_handler = logging.FileHandler(log_path)

    # Set the level and format
    console_handler.setLevel(logging.INFO)
    short_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.DEBUG)

    
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s [%(name)s at line %(lineno)d]')
    short_formatter = logging.Formatter('- %(levelname)s - %(message)s')
    console_handler.setFormatter(short_formatter)
    short_handler.setFormatter(file_formatter)
    file_handler.setFormatter(file_formatter)

    # Create the logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    logger.addHandler(short_handler)
    logger.addHandler(file_handler)

    return logger