from chatterbot.conversation import Statement
from chatterbot.trainers import ListTrainer


def test_db_count(test_adapter):
    expected = 50
    actual = test_adapter.count()

    assert expected is actual


def test_filter(test_adapter):
    statement = Statement("hi")

    kwargs = {
        "search_text_contains": statement.text
    }

    result = list(test_adapter.filter(**kwargs))
    assert len(result) > 0
    assert len(result) == 2


def test_create(test_adapter):
    statement_model = test_adapter.get_model("statement")

    kwargs = {
        "text": "bar",
        "in_response_to": "foo",
        "tags": "test"
    }

    result = test_adapter.create(**kwargs)

    s_text = kwargs.get("text")
    s_in_response_to = kwargs.get("in_response_to")

    assert result.text == s_text
    assert result.in_response_to == s_in_response_to

    session = test_adapter.Session()
    record = session.query(statement_model).filter(
        statement_model.text == s_text
    ).first()

    assert record.text == s_text

    test_adapter._session_finish(session)


def test_get_random(test_adapter):
    record = test_adapter.get_random()

    assert record is not None
    assert record.text is not None


# def test_update(test_bot):
#     question = "Hi"
#     updated = "foobar"
#
#     response = test_bot.get_bot_response(question)
#
#     kwargs = {
#         "updated_text": updated
#     }
#     test_bot.bot.storage.update(response, **kwargs)
#     response = test_bot.get_bot_response(question)
#
#     assert response.text == updated

def test_create_many(test_adapter):
    count = test_adapter.count()
    statements = []

    for i in range(20):
        s = Statement(str(i))
        s.in_response_to = str(i)
        statements.append(s)

    test_adapter.create_many(statements)

    assert test_adapter.count() == len(statements) + count
