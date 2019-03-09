import json
from chatbot import bot
from chatbot import constants


# Test whether the home page is accessible.
def test_home_page(test_client):
    result = test_client.get('/')
    assert result.status_code == 200


# Test whether the webhook returns the correct status codes.
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


# Test whether the chatbot can respond.
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
    bot.get_bot_response(question)
    alt_question = "ALT_RESPONSE, 1"
    response = bot.get_bot_response(alt_question)

    assert "greetings" in str(response).lower()


def test_feedback(init_bot):
    expected = ["good", "fine", "ok"]
    question = "how is it going?"

    for i in range(len(expected)):
        response = bot.get_bot_response(question)
        print(f"Expected: {expected[i]}, actual: {response} ")

        assert expected[i] in str(response).lower()

        bot.give_feedback(question, response.text, -1)


def test_bot_get_request(test_client):
    basic_msg = test_client.get('/', query_string={"msg": "hi"})
    alt_response_msg = test_client.get('/', query_string={"msg": "hello", "alt_response": "1"})
    feedback_msg = test_client.get('/', query_string={"msg": "FEEDBACK", "rating": "yes",
                                                      "question": "hello", "answer": "hi"})

    assert basic_msg.status_code == 200
    assert alt_response_msg.status_code == 200
    assert feedback_msg.status_code == 200

