from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.conversation import Statement
import logging

logging.basicConfig(level=logging.DEBUG)

bot = ChatBot(
    "C++ bot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database="botData.sqlite3"
)


def get_feedback():
    text = input()
    if 'y' in text.lower():
        return True
    elif 'n' in text.lower():
        return False
    else:
        print('Please type either "y" or "n"')
        return get_feedback()


should_train = input("Should I train? [y/n] ")
if should_train.lower() == "y":
    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train("data/data.yml")

# get user input and print a response
while True:
    try:
        user_input = input("\nYou: ")
        response = bot.get_response(user_input)
        print("{}: {}".format(bot.name, response))

        print('\nIs this a coherent response to "{}"? [y/n]'.format(user_input))

        if not get_feedback():
            print('Correct response:')
            correct_response = Statement(text=input())
            bot.learn_response(correct_response, Statement(user_input))
            print('Responses added to bot!')

    # press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        print("Exiting...")
        break

