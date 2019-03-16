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
                              data=json.dumps(dict(ref='refs/heads/master', test='true')),
                              content_type='application/json')
    assert result.status_code == 200
    assert b"Pulling from master" in result.data

    result = test_client.post('/webhook',
                              data=json.dumps(dict(ref='refs/heads/some_branch')),
                              content_type='application/json')
    assert result.status_code == 200
    assert b"Ignoring request" in result.data

    result = test_client.get('/webhook')
    assert result.status_code == 405 or result.status_code == 400
    assert b'The method is not allowed' in result.data


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
    response = test_bot.get_bot_response("ALT_RESPONSE")
    assert "greetings" in str(response).lower()

    test_bot.get_bot_response("Hi")
    response = test_bot.get_bot_response("ALT_RESPONSE")
    assert constants.BOT_NO_MORE_ANSWERS in str(response)


def test_feedback(test_bot):
    expected = ["good", "fine", "ok"]
    question = "how is it going?"

    for i in range(len(expected)):
        response = test_bot.get_bot_response(question)
        print(f"Expected: {expected[i]}, actual: {response} ")

        assert expected[i] in str(response).lower()

        test_bot.give_feedback(response.text, -1)


def test_bot_get_requests(test_client, test_bot):
    basic_msg = test_client.get('/get', query_string={'request_type': 'regular', 'msg': 'hello'})
    alt_response_msg = test_client.get('/get', query_string={"request_type": "alternate"})
    feedback_msg = test_client.get('/get', query_string={'request_type': 'feedback', 'rating': 'yes',
                                                         'answer': 'hi'})
    invalid = test_client.get('/get', query_string={"request_type": "foo", 'msg': 'bar'})

    assert basic_msg.status_code == 200
    assert b"Hi" in basic_msg.data

    assert alt_response_msg.status_code == 200
    assert b"Greetings" in alt_response_msg.data

    assert feedback_msg.status_code == 200
    assert b"OK" in feedback_msg.data

    assert invalid.status_code == 200
    assert b'Invalid request' in invalid.data
