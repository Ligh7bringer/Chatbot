import click
from flask.cli import with_appcontext
from chatbot.holder import bot


# fallback function to cancel a command
def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


# define command line commands: #

# crawl command, i.e. 'flask crawl'
@click.command('crawl', help="Collect training data from Stack Overflow.")
@click.option('-t', '--threads', default=3, help="Number of threads to be used when crawling.")
@click.option('-p', '--pages', default=1, help="Number of pages to be crawled by each thread.")
@click.option('-v', '--verbose', flag_value="True", help="Print more output.")
@with_appcontext
def crawl_command(threads, pages, verbose):
    click.echo(f"\nUsing {threads} threads\n"
               f"({pages} pages per thread)\n")
    bot.collect_data(threads, pages, verbose)


# train command, i.e. 'flask train'
@click.command('train', help="Train the chatbot with the data stored in /chatbot/training_data/")
@with_appcontext
def train_command():
    bot.train()


# delete command, i.e. 'flask del_db'
@click.command('del_db', help="DELETE the database the chatbot uses.")
@click.option('-y', '--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to DELETE the database?',
              help="Don't show confirmation prompt.")
@with_appcontext
def del_command():
    bot.del_db()


# clean command, i.e. 'flask clean'
@click.command('clean', help="DELETE the training data stored in /chatbot/training_data/")
@click.option('-y', '--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to DELETE the training data?',
              help="Don't show confirmation prompt.")
@with_appcontext
def clean_command():
    bot.clean()


# register command line commands
def init_app(app):
    app.cli.add_command(train_command)
    app.cli.add_command(crawl_command)
    app.cli.add_command(del_command)
    app.cli.add_command(clean_command)

