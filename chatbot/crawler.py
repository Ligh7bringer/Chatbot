import requests
from ruamel.yaml import YAML
from bs4 import BeautifulSoup
import threading
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import logging
import chatbot.constants as const
import os
import time


class Crawler:
    # initialises a crawler object
    def __init__(self, threads, pages, verbose):
        self.num_threads = threads
        self.num_pages = pages
        self.verbose_output = verbose
        # the following values can be changed if necessary: #
        # topic of the questions, e.g. 'java' or 'c++'
        self.tag = const.QUESTIONS_TAG
        # sort the questions by, e.g. 'highest rating'
        self.sort_by = const.SORT
        # number of questions per page
        self.page_size = const.PAGE_SIZE
        # the following variables are constant URLs: #
        self.page = const.PAGE
        self.page_size_url = const.PAGE_SIZE_URL
        # this array contains word which are removed from the titles
        self.to_clean = [" [duplicate]", " [closed]"]
        # the logger for this class
        self.logger = logging.getLogger(__name__)
        self.start_time = 0
        self.end_time = 0

    # removes some unnecessary words from the question title
    def clean_title(self, title):
        for word in self.to_clean:

            if word in title:
                self.logger.debug(f"Found{word} in {title}. Cleaning...")
                title = title.replace(word, "")

            return title

    # stores the training data into a .yaml file
    def write_to_file(self, data):
        # this is required so that the output file is in the correct format
        formatted_data = dict(categories=const.CATEGORIES, conversations=data)

        # create output folder
        if not os.path.exists(const.DATA_DIR_PATH):
            self.logger.warning(f"{const.DATA_DIR_PATH} does not exist. Creating it...")
            os.makedirs(const.DATA_DIR_PATH)

        # initialise yaml library
        yaml = YAML()
        yaml.default_flow_style = False
        # create output file
        out_file = os.path.join(const.DATA_DIR_PATH, str(threading.get_ident()) + const.FILE_EXT)

        self.logger.info(f"Writing to {out_file}...")

        # open the output file
        # encoding is important
        with open(out_file, 'w+', encoding="utf-8") as outfile:
            yaml.dump(formatted_data, outfile)

    # parses a question at a given URL
    def parse_question(self, url, title, data):
        # page to be scraped
        page = requests.get(url, headers=const.headers, timeout=(3, 30))
        # initialise bs4
        soup = BeautifulSoup(page.content, 'lxml')
        # get the question data, contained in a <div> with class "postcell"
        question = soup.find('div', class_='postcell')

        if question is not None:
            title = self.clean_title(title)
            # the question text is stored at index 1
            # question = list(question)[1].get_text()
            answers = soup.find_all('div', class_='answercell')
            # limit to max 3 answers per question
            end = len(answers)

            if end > const.CRAWLER_NUM_ANSWERS:
                end = const.CRAWLER_NUM_ANSWERS

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

    # crawls page(s) in the range [start, start + num_pages]
    def crawl_pages(self, num_pages, start):
        # a list to store the results
        data = []
        # define starting page
        current_page = start
        end = start + num_pages

        # while the target page hasn't been reached
        while current_page != end:
            try:
                # generate url of the page to be crawled
                page_url = const.BASE_URL + self.tag + self.sort_by + self.page + \
                           str(current_page) + self.page_size_url + str(self.page_size)
                # get its code
                source_code = requests.get(page_url, headers=const.headers, timeout=10).text
                # init bs4
                soup = BeautifulSoup(source_code, 'lxml')
                # print a message showing the url of the page being crawled
                self.logger.info(f"Crawling page {current_page}: {page_url}")
                q_no = 0

                # get a link to each question
                for ques_link in soup.find_all('a', {'class': 'question-hyperlink'}):
                    # make sure no extra links are crawled
                    if q_no == const.PAGE_SIZE:
                        break
                    # generate the link
                    url = const.SO_URL + ques_link.get('href')
                    # print question title for debugging purposes
                    title = ques_link.get_text()
                    self.logger.debug(title)
                    # parse this question
                    self.parse_question(url, title, data)
                    # keep track of current question number
                    q_no += 1
                # move on to the next page
                current_page += 1
            # catch some exceptions
            except (KeyboardInterrupt, EOFError, SystemExit):
                print("Aborted!")
                break

        self.end_time = time.time()
        self.logger.info(f"Crawling took {self.end_time - self.start_time}!")
        # print a message when done
        self.write_to_file(data)

    # start the crawling process
    def crawl(self):
        # set verbose to true/false based on what the user requested
        if self.verbose_output:
            self.logger.setLevel(level=logging.DEBUG)
        else:
            self.logger.setLevel(level=logging.INFO)

        # partial function so that more parameters can be passed
        # to the ThreadPoolExecutor
        func = partial(self.crawl_pages, self.num_pages)

        self.start_time = time.time()
        try:
            # create a ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
                # spawn num_threads threads
                for i in range(self.num_threads):
                    # create a future; divides the work equally between
                    # all threads
                    executor.submit(func, (i * self.num_pages + 1))
        except (KeyboardInterrupt, EOFError, SystemExit):
            self.logger.warning("Aborted!")

        self.logger.info("Done!")
