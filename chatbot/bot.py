import stat

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import click
from flask.cli import with_appcontext
from . import crawler
from chatbot.constants import *
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

cached_responses = []

# initialise chatbot
bot = ChatBot(
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
            'default_response':             BOT_NOT_UNDERSTAND,
            'maximum_similarity_threshold':  0.90
        },
        {
            'import_path':                  'chatbot.logic.SpecificResponseAdapter',
            'input_text':                   'Help',
            'output_text':                  BOT_HELP_MSG
        }
    ],
    database_uri='sqlite:///' + DB_FILE
)


def get_files(loc):
    files = []
    try:
        files = os.listdir(loc)
    except (FileNotFoundError, FileExistsError, OSError):
        logger.warning(f"{loc} does not exist or is empty. Skipping...")

    return files


# the functions below are called by the command line commands
def collect_data(threads, pages, verbose):
    crawler.run(threads, pages, verbose)


def train():
    trainer = ChatterBotCorpusTrainer(bot)

    try:
        trainer.train("chatterbot.corpus.english.greetings")
    except (OSError, FileExistsError, FileNotFoundError):
        logger.error("Couldn't find chatterbot-corpus! Are you sure it's installed?\n"
                     "(pip install chatterbot-corpus)")

    files = get_files(DATA_DIR_PATH)
    for file in files:
        trainer.train(os.path.join(DATA_DIR_PATH, file))


def del_db():
    try:
        os.remove(DB_FILE_PATH)
    except FileNotFoundError:
        logger.warning(f"{DB_FILE_PATH} does not exist.")
    except PermissionError:
        logger.warning(f"{DB_FILE_PATH} is open in another program and cannot be deleted.")
        os.chmod(DB_FILE_PATH, stat.S_IWRITE)
        os.remove(DB_FILE_PATH)


def clean():
    files = get_files(DATA_DIR_PATH)

    for file in files:
        os.remove(os.path.join(DATA_DIR_PATH, file))
    logger.info(f"Deleted {len(files)} files from {DATA_DIR_PATH}")
    try:
        os.rmdir(DATA_DIR_PATH)
    except (FileNotFoundError, OSError):
        logger.info(f"{DATA_DIR_PATH} does not exist. Skipping.")


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


# define command line commands
@click.command('crawl', help="Collect training data from Stack Overflow.")
@click.option('-t', '--threads', default=3, help="Number of threads to be used when crawling.")
@click.option('-p', '--pages', default=1, help="Number of pages to be crawled by each thread.")
@click.option('-v', '--verbose', flag_value="True", help="Print more output.")
@with_appcontext
def crawl_command(threads, pages, verbose):
    # click.echo("Verbose output is {}.".format('on' if verbose else 'off'))
    click.echo(f"\nUsing {threads} threads\n"
               f"({pages} pages per thread)\n")
    collect_data(threads, pages, verbose)


@click.command('train', help="Train the chatbot with the data stored in /chatbot/training_data/")
@with_appcontext
def train_command():
    train()


@click.command('del_db', help="DELETE the database the chatbot uses.")
@click.option('-y', '--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to DELETE the database?',
              help="Don't show confirmation prompt.")
@with_appcontext
def del_command():
    # click.echo("\n\nWARNING: The chatbot database will be DELETED.")
    del_db()


@click.command('clean', help="DELETE the training data stored in /chatbot/training_data/")
@click.option('-y', '--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to DELETE the training data?',
              help="Don't show confirmation prompt.")
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
    response = bot.get_response(question)

    pair = (question, response)
    cached_responses.append(pair)

    return response


def give_feedback(question, answer, rating):
    bot.storage.update_rating(question, answer, rating)
