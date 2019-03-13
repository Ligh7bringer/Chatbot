from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import git
import os
from chatbot.config import Config
from . import bot


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
        message = request.args.get('msg')
        alt_idx = request.args.get('alt_response')

        if alt_idx is not None and message is not "FEEDBACK":
            alt_idx = int(alt_idx)
            alt_question = "ALT_RESPONSE, " + str(alt_idx)
            app.logger.info("Alternate response requested")
            return str(bot.get_bot_response(alt_question))

        elif message == "FEEDBACK" and alt_idx is None:
            question = request.args.get('question')
            answer = request.args.get('answer')
            rating = request.args.get('rating')

            if rating == 'yes':
                value = 1
            else:
                value = -1

            app.logger.info("Feedback given.")
            bot.give_feedback(question, answer, value)
            return "OK"

        elif message is None:
            return "Invalid request"

        else:
            app.logger.info("Regular response requested.")
            return str(bot.get_bot_response(message))

    @app.route('/webhook', methods=['POST'])
    def webhook():
        if request.method == 'POST':
            data = request.get_json()
            branch = str(data.get('ref'))
            if branch == 'refs/heads/master':
                repo = git.Repo(os.getcwd())
                origin = repo.remotes.origin
                repo.create_head('master', origin.refs.master).set_tracking_branch(origin.refs.master).checkout()
                origin.pull()
                return 'Pulling from master...', 200
            else:
                return 'Ignoring request, branch is not master.', 200

        return 'Invalid request type.', 400

    @app.route("/")
    def home():
        return render_template("chatbot.html", title="Chatbot")

    @app.route("/about")
    def about():
        return render_template("about.html", title="About")

    bot.init_app(app)

    return app
