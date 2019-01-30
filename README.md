### A chatbot which can answer programming-related questions
Honours project 2018 - 2019

# Prerequisites
* Python 3
* pip

# Setup
1. Clone this repo and `` cd Chatbot/Bot/ ``
2. ``pip install -r requirements.txt``
 (you may want to create a **virtual environment** before running this command)
3. Set the environmental variables required by Flask:
 `` export FLASK_ENV=development; export FLASK_APP=chatbot ``

# Commands
After setting the enviromental variables, your options are:
* `` flask crawl `` - collects data from StackOverflow which can be later used for training the bot (stored in **chatbot/training_data/data.yml**)
* `` flask train `` - requires data collected from the above command. Trains the chatbot with the data
* `` flask del_db `` - **deletes** the database generated after training the chatbot
* `` flask run `` - runs a local server. The website can be accessed at **127.0.0.1:5000**