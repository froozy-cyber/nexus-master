#main.py
import sys
import logging
from ui.qt_app import run_app

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)-12s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('jarvis.log', encoding='utf-8'), 
        logging.StreamHandler(sys.stdout)
    ]
)

if __name__ == "__main__":
    run_app()
