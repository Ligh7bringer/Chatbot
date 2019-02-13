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
        userText = request.args.get('msg')
        return str(bot.get_bot_response(userText))

    @app.route('/webhook', methods=['POST'])
    def webhook():
        if request.method == 'POST':
            data = request.get_json()
            branch = str(data.get('ref'))
            if branch == 'refs/heads/release':
                r = git.Repo(os.getcwd())
                r.git.fetch()
                r.git.checkout('release')
                r.git.pull()
                return 'Pulling from release...', 200
            else:
                return 'Ignoring request, branch is not release.', 200

        return 'Invalid request type.', 400

    bot.init_app(app)

    return app
