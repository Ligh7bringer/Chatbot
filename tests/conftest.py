import pytest
from chatbot import create_app
from chatbot import bot


# Set up a test client so flask can be tested.
@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config['TESTING'] = True

    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


# Set up a test chatbot so that it can be tested.
@pytest.fixture(scope='module')
def init_bot():
    bot.collect_data(1, 1, False)
    bot.train()

    yield bot

    bot.del_db()
    bot.clean()

