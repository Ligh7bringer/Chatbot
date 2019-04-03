import os

import pytest
from chatbot import create_app, Bot
import chatbot.constants as const

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

    # establish an application context
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
    bot.clean()


# @pytest.fixture(scope="session", autouse=True)
# def cleanup(request):
#     """Cleanup a testing directory once we are finished."""
#     def remove_test_dir():
#         os.removedirs(const.DATA_DIR_PATH)
#         os.remove(const.DB_FILE_PATH)
#
#     request.addfinalizer(remove_test_dir)
