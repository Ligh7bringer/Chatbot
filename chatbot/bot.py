from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import click
from flask.cli import with_appcontext
from . import crawler
from chatbot.constants import *
import logging


logging.basicConfig(level=logging.INFO)


# initialise chatbot
bot = ChatBot(
    # name
    "C++ bot",
    read_only=True,
    # data will be stored in a database
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=[
        {
            'import_path':                  'chatbot.logic.best_match.BestMatch',
            'default_response':             'I am sorry, but I do not understand.',
            'maximum_similarity_threshold':  0.90
        },
        {
            'import_path':                  'chatbot.logic.specific_response.SpecificResponseAdapter',
            'input_text':                   'Help',
            'output_text':                  'You can type <b>help</b> to show this message. </br>'
                                            'After you ask a question, you can type <b>alternate response</b>'
                                            ' to get another answer if the original one wasn\'t helpful.'
        }
    ]
)


def get_files(loc):
    files = []
    try:
        files = os.listdir(loc)
    except (FileNotFoundError, FileExistsError, OSError):
        print(loc, "does not exist or is empty.")

    return files


# the functions below are called by the command line commands
def collect_data(threads, pages, verbose):
    crawler.run(threads, pages, verbose)


def train():
    trainer = ChatterBotCorpusTrainer(bot)

    try:
        trainer.train("chatterbot.corpus.english.greetings")
    except (OSError, FileExistsError, FileNotFoundError):
        print("Couldn't find chatterbot.corpus! Are you sure it's installed?")

    files = get_files(DATA_DIR_PATH)
    for file in files:
        trainer.train(os.path.join(DATA_DIR_PATH, file))


def del_db():
    try:
        os.remove(DB_FILE_PATH)
    except (FileNotFoundError, FileExistsError, OSError):
        print("File doesn't exist.")
        pass


def clean():
    files = get_files(DATA_DIR_PATH)

    for file in files:
        os.remove(os.path.join(DATA_DIR_PATH, file))
    print("Deleted {} files from {}".format(len(files), DATA_DIR_PATH))
    try:
        os.rmdir(DATA_DIR_PATH)
    except (FileNotFoundError, OSError):
        print(DATA_DIR_PATH, "does not exist. Skipping.")


# define command line commands
@click.command('crawl')
@click.option('-t', '--threads', default=3)
@click.option('-p', '--pages', default=1)
@click.option('-v', '--verbose', default=True)
@with_appcontext
def crawl_command(threads, pages, verbose):
    click.echo("\nCrawling with {} threads ({} pages per thread)\n".format(threads, pages))
    collect_data(threads, pages, verbose)


@click.command('train')
@with_appcontext
def train_command():
    train()


@click.command('del_db')
@with_appcontext
def del_command():
    click.echo("\n\nWARNING: The chatbot database will be DELETED.")
    del_db()


@click.command('clean')
@with_appcontext
def clean_command():
    clean()
    del_db()


# register command line commands
def init_app(app):
    app.cli.add_command(train_command)
    app.cli.add_command(crawl_command)
    app.cli.add_command(del_command)
    app.cli.add_command(clean_command)


# returns a response to a certain question
def get_bot_response(question):
    return bot.get_response(question)
