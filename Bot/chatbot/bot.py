from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import click
from flask.cli import with_appcontext
import os
from . import crawler


bot = ChatBot(
    "C++ bot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
)


def collect_data():
    crawler.run()


def train():
    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train("chatbot/training_data/data.yaml")


def del_db():
    os.remove("db.sqlite3")


@click.command('crawl')
@with_appcontext
def crawl_command():
    click.echo("Running crawler...")
    collect_data()


@click.command('train')
@with_appcontext
def train_command():
    click.echo("Training...")
    train()


@click.command('del_db')
@with_appcontext
def del_command():
    click.echo("WARNING: Deleting chatbot database...")
    del_db()


def init_app(app):
    app.cli.add_command(train_command)
    app.cli.add_command(crawl_command)
    app.cli.add_command(del_command)


def get_bot_response(question):
    return bot.get_response(question)
