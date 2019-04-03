import os

# File paths
PROJECT_ROOT = os.getcwd()
FLASK_APP_ROOT = os.path.join(PROJECT_ROOT, "chatbot")
DB_FILE = 'db'
DB_FILE_EXT = '.sqlite3'
DB_FILE_PATH = os.path.join(PROJECT_ROOT, DB_FILE + DB_FILE_EXT)
DATA_DIR = "training_data"
DATA_DIR_PATH = os.path.join(FLASK_APP_ROOT, DATA_DIR)

# Chatbot help message
BOT_HELP_MSG = '<ul class="fa-ul">' \
               '<li><span class="fa-li"><i class="fas fa-check"></i></span>You can type <b>help</b> in the chat or click the "Help" button in the ' \
               'menu at the top of the page to show this message. </li>' \
               '<li><span class="fa-li" ><i class="fas fa-check"></i></span>After you ask a question, you can type <b>alternate response</b> in the chat ' \
               'to get another answer to your last question. Alternatively, you can click the "Alternate response" button at the end of the original response.</li>' \
               '<li><span class="fa-li" ><i class="fas fa-check"></i></span>At the bottom of each message box, you are able to give feedback for each ' \
               'answer and you are encouraged to do so. This helps the bot answer questions more accurately!</li>' \
               '</ul>'

BOT_NOT_UNDERSTAND = "I am sorry, but I do not understand."
BOT_NO_MORE_ANSWERS = "Sorry, I don't know anything else about this."
BOT_NO_QUESTION = "You haven't asked any questions."

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
BASE_URL = 'https://stackoverflow.com/questions/tagged/'
# tag evaluates to c++
QUESTIONS_TAG = 'c%2b%2b'
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
