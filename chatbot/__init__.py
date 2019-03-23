import logging
import os
import git
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from chatbot.bot import Bot
from chatbot.config import Config
import chatbot.cli_interface
import chatbot.holder


# handle incoming requests
def handle_requests():
    logger = logging.getLogger(__name__)
    # get the request type
    request_type = request.args.get('request_type')
    logger.info(f"Request of type {request_type} received.")

    # request for alternate response
    if request_type == "alternate":
        # ask for an alternate response
        alt_question = "ALT_RESPONSE"
        logger.info("Alternate response requested.")

        return str(holder.bot.get_response(alt_question))

    # request to give feedback
    if request_type == "feedback":
        # get desired answer
        answer = request.args.get('answer')
        # get user's rating
        feedback = request.args.get('rating')
        logger.info("Feedback given.")

        # convert 'yes' to 1
        if feedback is 'yes':
            value = 1
        # anything else to -1
        else:
            value = -1

        # update the rating
        holder.bot.update_rating(answer, value)
        return "OK"

    # regular response requested
    if request_type == "regular":
        logger.info("Regular response requested.")
        # get the message
        message = request.args.get('msg')

        return str(holder.bot.get_response(message))

    # if this is reached, the request type was invalid
    return "Invalid request"


# deals with requests sent to /webhook
# which be coming from github
def handle_webhook():
    # only accept post requests
    if request.method == 'POST':
        # get data in json format
        data = request.get_json()
        # find out which branch was updated
        branch = str(data.get('ref'))

        # master contains the 'release' version
        if branch == 'refs/heads/master':
            # check if this is a test request,
            # sent from a unit test
            testing = request.get_json('test')

            # if it's not
            if testing is None:
                # pull from github!
                repo = git.Repo(os.getcwd())
                origin = repo.remotes.origin
                repo.create_head('master', origin.refs.master).set_tracking_branch(
                    origin.refs.master
                ).checkout()
                origin.pull()
            return 'Pulling from master...', 200
        else:
            return 'Ignoring request, branch is not master.', 200

    # if this is reached, the request was invalid
    return 'Invalid request type.', 400


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

    # define views: #

    # get requests will be sent to this endpoint
    @app.route("/get")
    def get_bot_response():
        return handle_requests()

    # webhook for automatic pull from github!
    @app.route('/webhook', methods=['POST'])
    def webhook():
        return handle_webhook()

    # home page
    @app.route("/")
    def home():
        # render the template
        return render_template("chatbot.html", title="Chatbot", show_title=False)

    # about page
    @app.route("/about")
    def about():
        # render the template
        return render_template("about.html", title="About This Project", show_title=True)

    # register command line interface
    cli_interface.init_app(app)

    # return the app
    return app
