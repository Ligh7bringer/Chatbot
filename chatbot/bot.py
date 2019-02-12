from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import click
from flask.cli import with_appcontext
import os
from . import crawler

PATH_TRAIN_DATA = os.path.join(os.getcwd(), 'chatbot/training_data/')
DB_NAME = "db.sqlite3"

# initialise chatbot
bot = ChatBot(
    # name
    "C++ bot",
    read_only=True,
    # data will be stored in a database
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    # preprocessors
    preprocessors= {
        "chatterbot.preprocessors.unescape_html"
    },
    logic_adapters=[
        {
            'import_path': 'chatbot.logic_adapter.BestMatch'
        }
    ]
)


def get_files(dir):
    files = []
    try:
        files = os.listdir(dir)
    except (FileNotFoundError, FileExistsError, OSError):
        print(dir, "does not exist or is empty.")

    return files


# the functions below are called by the command line commands
def collect_data(threads, pages, verbose):
    crawler.run(threads, pages, verbose)


def train():
    trainer = ChatterBotCorpusTrainer(bot)
    try:
        trainer.train("chatterbot.corpus.english.greetings")
    except (OSError, FileExistsError, FileNotFoundError):
        print("Couldn't find chatterbot.corpus! Are you sure its installed?")

    files = get_files(PATH_TRAIN_DATA)
    for file in files:
        trainer.train(os.path.join(PATH_TRAIN_DATA, file))


def del_db():
    try:
        os.remove(os.path.join(os.getcwd(), DB_NAME))
    except (FileNotFoundError, FileExistsError, OSError):
        print("File doesn't exist.")
        pass


def clean():
    files = get_files(PATH_TRAIN_DATA)

    for file in files:
        os.remove(os.path.join(PATH_TRAIN_DATA, file))
    print("Deleted {} files from {}".format(len(files), PATH_TRAIN_DATA))
    try:
        os.rmdir(PATH_TRAIN_DATA)
    except (FileNotFoundError, OSError):
        print(PATH_TRAIN_DATA, "does not exist. Skipping.")


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
