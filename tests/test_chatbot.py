import json
from chatbot import constants


# Test whether the home page is accessible.
def test_home_page(test_client):
    result = test_client.get('/')
    assert result.status_code == 200

    result = test_client.get('/about')
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
def test_bot_response(test_bot):
    question = "hi"
    response = test_bot.get_bot_response(question)

    assert "hello" or "hi" in str(response).lower()

    question = "How to make an omelette?"
    response = test_bot.get_bot_response(question)
    assert constants.BOT_NOT_UNDERSTAND in str(response)


def test_help_response(test_bot):
    help_question = "Help"
    response = test_bot.get_bot_response(help_question)

    assert constants.BOT_HELP_MSG in str(response)


def test_alternate_response(test_bot):
    test_bot.get_bot_response("Hello")
    response = test_bot.get_bot_response("ALT_RESPONSE, 1")
    assert "greetings" in str(response).lower()

    test_bot.get_bot_response("Hi")
    response = test_bot.get_bot_response("ALT_RESPONSE, 1")
    assert constants.BOT_NO_MORE_ANSWERS in str(response)


def test_feedback(test_bot):
    expected = ["good", "fine", "ok"]
    question = "how is it going?"

    for i in range(len(expected)):
        response = test_bot.get_bot_response(question)
        print(f"Expected: {expected[i]}, actual: {response} ")

        assert expected[i] in str(response).lower()

        test_bot.give_feedback(question, response.text, -1)


def test_bot_get_request(test_client):
    basic_msg = test_client.get('/', query_string={"msg": "hi"})
    alt_response_msg = test_client.get('/', query_string={"msg": "hello", "alt_response": "1"})
    feedback_msg = test_client.get('/', query_string={"msg": "FEEDBACK", "rating": "yes",
                                                      "question": "hello", "answer": "hi"})

    assert basic_msg.status_code == 200
    assert alt_response_msg.status_code == 200
    assert feedback_msg.status_code == 200

