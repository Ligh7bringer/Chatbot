from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import click
from flask.cli import with_appcontext
from . import crawler


bot = ChatBot(
    "C++ bot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    )


def collect_data():
    crawler.run()


def train():
    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train("chatbot/training_data/data.yml")


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


def init_app(app):
    app.cli.add_command(train_command)
    app.cli.add_command(crawl_command)


def get_bot_response(question):
    return bot.get_response(question)
