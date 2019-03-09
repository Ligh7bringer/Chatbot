import os

# File paths
PROJECT_ROOT = os.getcwd()
FLASK_APP_ROOT = os.path.join(PROJECT_ROOT, "chatbot")
DB_FILE = "db.sqlite3"
DB_FILE_PATH = os.path.join(PROJECT_ROOT, DB_FILE)
DATA_DIR = "training_data"
DATA_DIR_PATH = os.path.join(FLASK_APP_ROOT, DATA_DIR)

# Chatbot help message
BOT_HELP_MSG = 'You can type <b>help</b> to show this message. ' \
               '</br> After you ask a question, you can type <b>alternate response</b> ' \
               'to get another answer if the original one wasn\'t helpful.'

# Crawler constants:
# how many answers to be scraped from every question
CRAWLER_NUM_ANSWERS = 3
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/53.0.2785.143 Safari/537.36 '
}

# stack overflow
SO_URL = 'http://stackoverflow.com/'
# questions tagged 'c++'
BASE_URL = 'https://stackoverflow.com/questions/tagged/c%2b%2b'
# sort by votes
SORT = '?sort=votes'
# current page
PAGE = '&page='
# how many questions per page
PAGE_SIZE_URL = '&pageSize='
# how many questions per page
PAGE_SIZE = 10
# results file name
FILE_EXT = '.yaml'
CATEGORIES = ["StackOverflow", "C++"]
SCRAPE_FORMATTING = True
