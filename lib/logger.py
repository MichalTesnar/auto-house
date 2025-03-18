import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.DEBUG,  # Set the base logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler("logs/app.log", maxBytes=1024 * 1024 * 5, backupCount=5),  # 5 MB per file, 5 backups
        logging.StreamHandler(),  # Log to console
    ],
)

logger = logging.getLogger(__name__)