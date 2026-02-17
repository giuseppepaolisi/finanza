import logging
import sys
from logging import handlers
from pathlib import Path

def setup_logger(name: str = "finanza"):
    logger = logging.getLogger(name)
    # Controlla che se il file log/finanza.log esiste
    file = Path("logs/finanza.log")
    if not file.exists():
        file.parent.mkdir(parents=True, exist_ok=True)
    
    # Evitia di aggiungere handler multipli se la funzione viene richiamata
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Handler Console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)

        # Handler File
        file_handler = handlers.TimedRotatingFileHandler("logs/finanza.log", when="midnight", backupCount=7)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
        # Impedisce ai log di propagarsi al root logger di default (evita doppi log con Uvicorn)
        logger.propagate = False

    return logger