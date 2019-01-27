### A chatbot which can answer programming-related questions
Honours project 2018 - 2019

# Prerequisites
* Python 3
* pip

# Setup
1. Clone this repo
2. `` pip install -r requirements
export FLASK_APP=chatbot.txt ``
 You may prefer to crete a **virtual environment** before downloading the libraries.
3. Set required environmental variables:
 `` export FLASK_ENV=development ``
 `` export FLASK_APP=chatbot ``
 (**NOTE:** this will only set the variables for the current shell)

# Commands
After setting the enviromental variables, your options are:
* `` flask crawl `` - collects data from StackOverflow which can be later used for training the bot (stored in **chatbot/training_data/data.yml**)
* `` flask train `` - requires data collected from the above command. Trains the chatbot with the data.
* `` flask run `` - runs a local server. The website can be accessed at **127.0.0.1:5000**