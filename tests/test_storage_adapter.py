from chatterbot.conversation import Statement


# Tests whether to number of rows in the database can be counted.
def test_db_count(test_adapter):
    expected = 50
    actual = test_adapter.count()

    assert expected is actual


# Tests whether SELECT ... FROM queries work.
def test_filter(test_adapter):
    statement = Statement("hi")

    kwargs = {
        "search_text_contains": statement.text
    }

    result = list(test_adapter.filter(**kwargs))
    assert len(result) == 2


# Tests whether new entries can be added to the database.
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


# Tests whether a random record from the database can be retrieved.
def test_get_random(test_adapter):
    record = test_adapter.get_random()

    assert record is not None
    assert record.text is not None


# Tests if many entries can be added to the database.
def test_create_many(test_adapter):
    count = test_adapter.count()
    statements = []

    for i in range(20):
        s = Statement(str(i))
        s.in_response_to = str(i)
        statements.append(s)

    test_adapter.create_many(statements)

    assert test_adapter.count() == len(statements) + count


# Tests whether a database entry can be updated.
def test_update(test_bot):
    question = "Hi"
    updated = "foobar"

    response = test_bot.get_response(question)

    kwargs = {
        "updated_text": updated
    }
    test_bot.chatbot.storage.update(response, **kwargs)

    kwargs = {
        "search_text_contains": updated
    }
    result = list(test_bot.chatbot.storage.filter(**kwargs))

    assert result is not None


# Tests if a database entry can be removed.
def test_remove(test_adapter):
    stmnt_model = test_adapter.get_model('statement')
    session = test_adapter.Session()

    all_records = session.query(stmnt_model).all()
    initial_count = len(all_records)

    test_adapter.remove("Hello")
    all_records = session.query(stmnt_model).all()
    count = len(all_records)

    assert initial_count > count


# Test if the database tables can be dropped.
def test_drop(test_adapter):
    stmnt_model = test_adapter.get_model('statement')
    session = test_adapter.Session()

    all_records = session.query(stmnt_model).all()
    initial_count = len(all_records)

    assert initial_count > 0

    test_adapter.drop()
    all_records = session.query(stmnt_model).all()

    assert len(all_records) is 0

