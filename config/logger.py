import logging
import os
from config.settings import LOG_DIR


os.makedirs(LOG_DIR, exist_ok=True)



LOG_FILE = os.path.join(LOG_DIR, "etl_pipeline.log")



logger = logging.getLogger("RetailPulse_ETL")
logger.setLevel(logging.INFO)



if not logger.handlers:


    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    # Console handler
    console_handler = logging.StreamHandler()

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)