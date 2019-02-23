import json
from chatbot import bot
from chatbot import constants

"""
Test whether the home page is accessible.
"""
def test_home_page(test_client):
    result = test_client.get('/')
    assert result.status_code == 200


"""
Test whether the webhook returns the correct status codes.
"""
def test_webhook(test_client):
    result = test_client.post('/webhook',
                              data=json.dumps(dict(ref='refs/head/master')),
                              content_type='application/json')
    assert result.status_code == 200
    # assert "Pulling from release" in result.output

    result = test_client.post('/webhook',
                              data=json.dumps(dict(ref='refs/heads/some_branch')),
                              content_type='application/json')
    assert result.status_code == 200
    # assert "Ignoring request" in result.output

    result = test_client.get('/webhook')
    assert result.status_code == 405 or result.status_code == 400


"""
Test whether the chatbot can respond.
"""
def test_bot_response(init_bot):
    question = "hi"
    response = bot.get_bot_response(question)

    assert "hello" or "hi" in str(response).lower()


def test_help_response(init_bot):
    help_question = "Help"
    response = bot.get_bot_response(help_question)

    assert constants.BOT_HELP_MSG in str(response)


def test_alternate_response(init_bot):
    question = "Hello"
    response = bot.get_bot_response(question)
    alt_question = "ALT_RESPONSE, 1"
    response = bot.get_bot_response(alt_question)

    assert "greetings" in str(response).lower()


def test_bot_get_request(test_client):
    result = test_client.get('/?msg=hi')
    
    assert result.status_code == 200