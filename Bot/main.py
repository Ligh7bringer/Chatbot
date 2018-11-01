# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from settings import TWITTER
import logging

# enable verbose logging
logging.basicConfig(level=logging.INFO)

# create chatbot instance and set it up to use the Twitter trainer
chatbot = ChatBot(
    "TwitterBot",
    logic_adapters=[
        "chatterbot.logic.BestMatch",
        # "chatterbot.logic.MathematicalEvaluation",
        # "chatterbot.logic.TimeLogicAdapter",
        # {
        #     'import_path': 'chatterbot.logic.LowConfidenceAdapter',
        #     'threshold': 0.65,
        #     'default_response': 'I am sorry, but I do not understand.'
        # }
    ],
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace',
    ],
    database_uri="sqlite:///db.sqlite3",
    twitter_consumer_key=TWITTER["CONSUMER_KEY"],
    twitter_consumer_secret=TWITTER["CONSUMER_SECRET"],
    twitter_access_token_key=TWITTER["ACCESS_TOKEN"],
    twitter_access_token_secret=TWITTER["ACCESS_TOKEN_SECRET"],
    trainer='custom_trainer.TwitterTrainer',
    twitter_lang="en",
    random_seed_word="hi"
)

# train
chatbot.train()

# get user input and print a response
while True:
    try:
        user_input = input("\nYou: ")
        response = chatbot.get_response(user_input)
        print("{}: {}".format(chatbot.name, response))

    # press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
