import logging
import stat
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os
import chatbot.constants as const
from chatbot.crawler import Crawler


class Bot:
    def __init__(self, db=None):
        # custom database name in the event that
        # multiple chatbots need to exist
        if db is None:
            self.db = const.DB_FILE + const.DB_FILE_EXT
        else:
            self.db = db + const.DB_FILE_EXT

        # store path to the database
        self.db_path = os.path.join(const.PROJECT_ROOT, self.db)

        # initialise chatbot
        self.chatbot = ChatBot(
            # name
            "C++ bot",
            read_only=True,
            storage_adapter="chatbot.storage.SQLStorageAdapter",
            preprocessors=[
                'chatterbot.preprocessors.unescape_html'
            ],
            logic_adapters=[
                {
                    'import_path':                  'chatbot.logic.BestMatch',
                    'default_response':             const.BOT_NOT_UNDERSTAND,
                    'maximum_similarity_threshold':  0.90
                },
                {
                    'import_path':                  'chatbot.logic.SpecificResponseAdapter',
                    'input_text':                   'Help',
                    'output_text':                  const.BOT_HELP_MSG
                }
            ],
            database_uri='sqlite:///' + self.db
        )
        self.logger = self.chatbot.logger
        logging.basicConfig(level=logging.INFO)

    # returns a list of files in directory 'loc'
    def get_files(self, loc):
        files = []
        try:
            files = os.listdir(loc)
        except (FileNotFoundError, FileExistsError, OSError):
            self.logger.warning(f"{loc} does not exist or is empty. Skipping...")

        return files

    # trains the chatbot
    def train(self):
        # initialise trainer
        trainer = ChatterBotCorpusTrainer(self.chatbot)

        # make sure chatterbot-corpus is installed
        try:
            trainer.train("chatterbot.corpus.english.greetings")
        # show an error message if it's not
        except (OSError, FileExistsError, FileNotFoundError):
            self.logger.error("Couldn't find chatterbot-corpus! Are you sure it's installed?\n"
                              "(try pip install chatterbot-corpus)")

        # get the file names of files made by the crawler
        files = self.get_files(const.DATA_DIR_PATH)
        # iterate over them
        for file in files:
            # train the chatbot with each file
            trainer.train(os.path.join(const.DATA_DIR_PATH, file))

    # returns a response to statement 'statement'
    def get_response(self, question):
        return self.chatbot.get_response(question)

    # updates the rating for answer 'answer'
    def update_rating(self, answer, rating):
        self.chatbot.storage.update_rating(answer, rating)

    # initialises and runs a crawler to collect data
    def collect_data(self, threads, pages, verbose):
        crawler = Crawler(threads, pages, verbose)
        crawler.crawl()

    # deletes the database
    def del_db(self):
        try:
            os.remove(self.db_path)
        except FileNotFoundError:
            self.logger.warning(f"{self.db_path} does not exist.")
        # try and gain permissions to delete the file
        except PermissionError:
            self.logger.warning(f"{self.db_path} is open in another program and cannot be deleted.")
            os.chmod(self.db_path, stat.S_IWRITE)
            os.remove(self.db_path)

    # deletes the training data
    def clean(self):
        files = self.get_files(const.DATA_DIR_PATH)

        for file in files:
            os.remove(os.path.join(const.DATA_DIR_PATH, file))

        self.logger.info(f"Deleted {len(files)} files from {const.DATA_DIR_PATH}")

        try:
            os.rmdir(const.DATA_DIR_PATH)
        except (FileNotFoundError, OSError):
            self.logger.info(f"{const.DATA_DIR_PATH} does not exist. Skipping.")
