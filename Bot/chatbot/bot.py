from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import click
from flask.cli import with_appcontext
import os
from . import crawler

# initialise chatbot
bot = ChatBot(
    # name
    "C++ bot",
    # data will be stored in a database
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    # preprocessors
    preprocessors= {
        "chatterbot.preprocessors.unescape_html"
    },
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.'
        }
    ]
)


# the functions below will be used for command line commands
def collect_data():
    crawler.run()


def train():
    PATH = 'chatbot/training_data/'

    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train("chatterbot.corpus.english.greetings")

    files = os.listdir(PATH)
    if files is None:
        print("No files found in", PATH)
    else:
        for file in files:
            trainer.train(PATH + file)


def del_db():
    os.remove("db.sqlite3")


# define command line commands
@click.command('crawl')
@with_appcontext
def crawl_command():
    click.echo("\nRunning crawler...")
    collect_data()


@click.command('train')
@with_appcontext
def train_command():
    click.echo("\nTraining...")
    train()


@click.command('del_db')
@with_appcontext
def del_command():
    click.echo("\n\nWARNING: The chatbot database will be DELETED.")
    response = input("Are you sure? [y/n]   ")
    if response.lower() == 'y':
        del_db()


# register command line commands
def init_app(app):
    app.cli.add_command(train_command)
    app.cli.add_command(crawl_command)
    app.cli.add_command(del_command)


# returns a response to a certain question
def get_bot_response(question):
    return bot.get_response(question)
