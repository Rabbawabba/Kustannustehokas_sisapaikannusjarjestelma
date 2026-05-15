import logging
import os
from datetime import datetime

# Asetetaan lokihakemisto projektin juureen
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
os.makedirs(log_dir, exist_ok=True)

def setup_logger(name, log_file, level=logging.INFO):
    """
    Alustaa loggerin, joka kirjoittaa lokit sekä tiedostoon että konsoliin.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.hasHandlers():
        logger.handlers.clear()

    # Tiedostoloki
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

    # Konsoliloki
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(console_handler)

    return logger

# Luo error_logger, joka kirjoittaa päivämäärän mukaan nimettyyn tiedostoon
log_file_name = f"error_{datetime.now().strftime('%Y-%m-%d')}.log"
log_file_path = os.path.join(log_dir, log_file_name)
error_logger = setup_logger('error', log_file_path)