from flask import Flask, render_template, request
import git
import os
from . import bot

''' 
Sets up the flask app.
'''


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/get")
    def get_bot_response():
        user_text = request.args.get('msg')
        alt_idx = request.args.get('alt_response')

        if alt_idx is not None:
            alt_idx = int(alt_idx)
            alt_question = "ALT_RESPONSE, " + str(alt_idx)
            app.logger.info(alt_question)
            return str(bot.get_bot_response(alt_question))

        app.logger.info("RESPONSE REQUESTED")
        return str(bot.get_bot_response(user_text))

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

    bot.init_app(app)

    return app
