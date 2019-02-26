import os

PROJECT_ROOT = os.getcwd()
FLASK_APP_ROOT = os.path.join(PROJECT_ROOT, "chatbot")
DB_FILE = "db.sqlite3"
DB_FILE_PATH = os.path.join(PROJECT_ROOT, DB_FILE)
DATA_DIR = "training_data"
DATA_DIR_PATH = os.path.join(FLASK_APP_ROOT, DATA_DIR)
BOT_HELP_MSG = 'You can type <b>help</b> to show this message. ' \
               '</br> After you ask a question, you can type <b>alternate response</b> ' \
               'to get another answer if the original one wasn\'t helpful.'
CRAWLER_NUM_ANSWERS = 3
