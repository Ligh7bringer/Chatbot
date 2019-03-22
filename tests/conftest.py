import pytest
from chatbot import create_app, Bot

###################
# PyTest fixtures #
###################


# Set up a test client so flask can be tested.
@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config['TESTING'] = True
    testing_client = flask_app.test_client()

    bot = Bot()
    bot.train()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()

    bot.clean()
    bot.del_db()


# Set up a test chatbot so that it can be tested.
@pytest.fixture(scope='module')
def test_bot():
    bot = Bot()
    bot.collect_data(1, 1, False)
    bot = Bot()

    yield bot

    bot.del_db()
    bot.clean()


# Set up a test storage adapter so that it can be tested.
@pytest.fixture(scope='module')
def test_adapter():
    bot = Bot()
    bot.train()
    adapter = bot.chatbot.storage

    # test
    yield adapter

    # delete the database
    bot.del_db()
