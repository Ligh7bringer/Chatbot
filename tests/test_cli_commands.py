import click
import os
from chatbot.run_it import app
from chatbot.bot import train_command
from chatbot.bot import del_command
from chatbot.bot import crawl_command
from chatbot.bot import clean_command


"""
Create a test command ensure pytest is working.
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
    threads = 1
    pages = 1
    runner = app.test_cli_runner()
    result = runner.invoke(crawl_command, ['--threads', threads, '--pages', pages, '--verbose', False])

    # assert 'Crawling with 1 threads (1 pages per thread)' in result.output

    files = os.listdir('chatbot/training_data')
    assert len(files) > 0
    assert len(files) == threads


"""
Tests whether the chatbot can be trained using the 'train' command
"""
def test_train():
    runner = app.test_cli_runner()
    result = runner.invoke(train_command)

    # assert training was successful
    assert "Done" in result.output
    
    # assert that the db file was created
    exists = os.path.isfile('db.sqlite3')
    assert exists is True


"""
Tests that the database can be deleted using the 'del_db' command.
"""
def test_del_db():
    runner = app.test_cli_runner()
    result = runner.invoke(del_command)
    
    assert not os.path.exists('db.sqlite3')


"""
Tests that the training files can be deleted using the 'clean' command.
"""
def test_clean():
    runner = app.test_cli_runner()
    result = runner.invoke(clean_command)

    files = os.listdir('chatbot/training_data/')
    assert len(files) is 0
