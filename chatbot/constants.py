import os

PROJECT_ROOT = os.getcwd()
FLASK_APP_ROOT = os.path.join(PROJECT_ROOT, "chatbot")
DB_FILE = "db.sqlite3"
DB_FILE_PATH = os.path.join(PROJECT_ROOT, DB_FILE)
DATA_DIR = "training_data"
DATA_DIR_PATH = os.path.join(FLASK_APP_ROOT, DATA_DIR)
