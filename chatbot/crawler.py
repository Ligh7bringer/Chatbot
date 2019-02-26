import requests
from ruamel.yaml import YAML
from bs4 import BeautifulSoup
import threading
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from chatbot.constants import *


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/53.0.2785.143 Safari/537.36 '
}

''' URLs '''
# stack overflow
SO_URL = 'http://stackoverflow.com/'
# question tagged 'c++'
BASE_URL = 'https://stackoverflow.com/questions/tagged/c%2b%2b'
# sort by votes
SORT = '?sort=votes'
# current page
PAGE = '&page='
# how many questions per page
PAGE_SIZE_URL = '&pageSize='
''' --- '''
# how many questions per page
PAGE_SIZE = 10
# how many answers to be scraped from every question
NUM_ANSWERS = 3
# results file name
FILE_EXT = '.yaml'
CATEGORIES = ["StackOverflow", "C++"]
VERBOSE_OUTPUT = True
SCRAPE_FORMATTING = True


# writes the scraped data in yaml format in a file
def write_to_file(data):
    final_data = dict(categories=CATEGORIES, conversations=data)
    # create output folder
    if not os.path.exists(DATA_DIR_PATH):
        os.makedirs(DATA_DIR_PATH)
    # initialise yaml library
    yaml = YAML()
    yaml.default_flow_style = False
    # create output file
    out_file = os.path.join(DATA_DIR_PATH, str(threading.get_ident()) + FILE_EXT)
    if VERBOSE_OUTPUT is True:
        print("Writing to", out_file)
    with open(out_file, 'w+') as outfile:
        yaml.dump(final_data, outfile)


# extracts the question text and a list of answers from a single question on StackOverflow
def parse_question(url, title, data):
    # page to be scraped
    page = requests.get(url, headers=headers, timeout=(3, 30))
    # initialise bs4
    soup = BeautifulSoup(page.content, 'lxml')
    # get the question data, contained in a <div> with class "postcell"
    question = soup.find('div', class_='postcell')
    if question is not None:
        # the question text is stored at index 1
        # question = list(question)[1].get_text()
        answers = soup.find_all('div', class_='answercell')
        # limit to max 3 answers per question
        end = len(answers)
        if end > CRAWLER_NUM_ANSWERS:
            end = CRAWLER_NUM_ANSWERS
        # for each answer found
        for i in range(0, end):
            # get the answer text
            answer = answers[i].find('div', class_='post-text').extract()
            # store the question and the answer in their own list
            answer = str(answer)
            entry = [title, answer]
            # add to the main list
            data.append(entry)


# gets the links to all questions on a page of StackOverflow
def crawl_pages(num_pages, start):
    # a list to store the results
    data = []
    # define starting page
    current_page = start
    end = start + num_pages
    # while the target page hasn't been reached
    while current_page != end:
        try:
            # generate url of the page to be crawled
            page_url = BASE_URL + SORT + PAGE + str(current_page) + PAGE_SIZE_URL + str(PAGE_SIZE)
            # get its code
            source_code = requests.get(page_url, headers=headers, timeout=10).text
            # init bs4
            soup = BeautifulSoup(source_code, 'lxml')
            # print a message showing the url of the page being crawled
            if VERBOSE_OUTPUT is True:
                print('crawling page ' + str(current_page) + ': ' + page_url + '\n')
            q_no = 0
            # get a link to each question
            for ques_link in soup.find_all('a', {'class': 'question-hyperlink'}):
                # make sure no extra links are crawled
                if q_no == PAGE_SIZE:
                    break
                # generate the link
                url = SO_URL + ques_link.get('href')
                # print question title for debugging purposes
                title = ques_link.get_text()
                if VERBOSE_OUTPUT is True:
                    print(title)
                # parse this question
                parse_question(url, title, data)
                # keep track of current question number
                q_no += 1
            # move on to the next page
            current_page += 1
        # catch some exceptions
        except (KeyboardInterrupt, EOFError, SystemExit):
            print("\nStopped by user!")
            break
    # print a message when done
    print('\nDone crawling!')
    write_to_file(data)


def run(workers, num_pages, verbose):
    global VERBOSE_OUTPUT
    VERBOSE_OUTPUT = verbose
    # number of pages each thread will crawl
    num_pages = int(num_pages)
    # number of threads
    workers = int(workers)
    func = partial(crawl_pages, num_pages)
    try:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            for i in range(workers):
                future = executor.submit(func, (i * num_pages + 1))
    except (KeyboardInterrupt, EOFError, SystemExit):
        print("Interrupted...")

    print("\nDone crawling!")
