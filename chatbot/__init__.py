from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import git
import os
from chatbot.bot import Bot
from chatbot.config import Config
from . import cli_interface
from chatbot.holder import bot
# Sets up the flask app.
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    bootstrap = Bootstrap(app)

    app.config.from_object(Config)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    @app.route("/get")
    def get_bot_response():
        # get the request type
        request_type = request.args.get('request_type')
        app.logger.info(f"Request of type {request_type} received.")

        if request_type == "alternate":
            alt_question = "ALT_RESPONSE"
            app.logger.info("Alternate response requested.")

            return str(bot.get_response(alt_question))

        if request_type == "feedback":
            answer = request.args.get('answer')
            feedback = request.args.get('rating')
            app.logger.info("Feedback given.")

            # convert 'yes' to 1
            if feedback is 'yes':
                value = 1
            # anything else to -1
            else:
                value = -1

            bot.update_rating(answer, value)
            return "OK"

        if request_type == "regular":
            app.logger.info("Regular response requested.")
            # get the message
            message = request.args.get('msg')

            return str(bot.get_response(message))

        # if this code is reached,
        # the request type was invalid
        return "Invalid request"

    @app.route('/webhook', methods=['POST'])
    def webhook():
        if request.method == 'POST':
            data = request.get_json()
            branch = str(data.get('ref'))

            if branch == 'refs/heads/master':
                testing = request.get_json('test')

                if testing is None:
                    repo = git.Repo(os.getcwd())
                    origin = repo.remotes.origin
                    repo.create_head('master', origin.refs.master).set_tracking_branch(
                        origin.refs.master
                    ).checkout()
                    origin.pull()
                return 'Pulling from master...', 200
            else:
                return 'Ignoring request, branch is not master.', 200

        return 'Invalid request type.', 400

    @app.route("/")
    def home():
        return render_template("chatbot.html", title="Chatbot", show_title=False)

    @app.route("/about")
    def about():
        return render_template("about.html", title="About", show_title=True)

    cli_interface.init_app(app)

    return app
