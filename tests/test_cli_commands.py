import click
from chatbot.run_it import app
from chatbot.bot import train_command
from chatbot.bot import del_command
from chatbot.bot import crawl_command
from chatbot.bot import clean_command
from chatbot.constants import *

"""
Usage: run pytest from the project root (the tests will be discovered automatically)
These tests do not use fixtures and assume a clean project folder.
That is, the database file and training data should NOT exist prior to running them.
This is the case as they are only run from travis-CI.
"""


"""
Create a test command to ensure pytest is working.
"""
@app.cli.command('hello')
@click.option('--name', default='World')
def hello_command(name):
    click.echo(f'Hello, {name}!')


"""
Test the sample command defined above.
"""
def test_hello():
    runner = app.test_cli_runner()

    # invoke the command directly
    result = runner.invoke(hello_command, ['--name', 'Flask'])
    assert 'Hello, Flask' in result.output

    # or by name
    result = runner.invoke(args=['hello'])
    assert 'World' in result.output


"""
Tests whether the crawl command works.
"""
def test_crawl():
    threads = 2
    pages = 1
    runner = app.test_cli_runner()
    result = runner.invoke(crawl_command, ['--threads', threads, '--pages', pages, '--verbose', False])

    assert result.output.count("{} threads".format(threads)) == 1
    assert result.output.count("{} pages".format(pages)) == 1

    files = os.listdir(DATA_DIR_PATH)
    num_files = len(files)
    assert num_files > 0
    assert num_files == threads


"""
Tests whether the chatbot can be trained using the 'train' command.
"""
def test_train():
    runner = app.test_cli_runner()
    result = runner.invoke(train_command)

    # assert training was successful
    assert "Couldn't find chatterbot.corpus" not in result.output

    # assert that the db file was created
    db_exists = os.path.isfile(DB_FILE_PATH)
    assert db_exists is True


"""
Tests that the database can be deleted using the 'del_db' command.
"""
def test_del_db():
    runner = app.test_cli_runner()
    runner.invoke(del_command)

    assert not os.path.exists(DB_FILE_PATH)


"""
Tests that the training files can be deleted using the 'clean' command.
"""
def test_clean():
    runner = app.test_cli_runner()
    runner.invoke(clean_command)

    assert not os.path.exists(DATA_DIR_PATH)
