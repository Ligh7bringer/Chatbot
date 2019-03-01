# :zap: Honours Project 2018 - 2019 :zap:
A chatbot which can answer C++ questions based on data collected from [Stack Overflow](https://stackoverflow.com/questions/tagged/c%2b%2b?sort=votes&pageSize=15).

# Repo Status
| **Branch**      | **CI**                                                       | **Code coverage**                                            | **Requirements**                                             | **Maintainability**                                          |
|-----------------|---|---|---|---|
| master |[![Build Status](https://travis-ci.org/Ligh7bringer/Chatbot.svg?branch=master)](https://travis-ci.org/Ligh7bringer/Chatbot)|[![Code Coverage](https://codecov.io/github/Ligh7bringer/Chatbot/branch/master/graphs/badge.svg)](https://codecov.io/github/Ligh7bringer/Chatbot)|[![Requirements Status](https://requires.io/github/Ligh7bringer/Chatbot/requirements.svg?branch=master)](https://requires.io/github/Ligh7bringer/Chatbot/requirements/?branch=master)|[![Maintainability](https://api.codeclimate.com/v1/badges/b1106d6c1e2f197d07ba/maintainability)](https://codeclimate.com/github/Ligh7bringer/Chatbot/maintainability)|
| development |[![Build Status](https://travis-ci.org/Ligh7bringer/Chatbot.svg?branch=dev)](https://travis-ci.org/Ligh7bringer/Chatbot)|[![Code Coverage](https://codecov.io/github/Ligh7bringer/Chatbot/branch/dev/graphs/badge.svg)](https://codecov.io/github/Ligh7bringer/Chatbot)|[![Requirements Status](https://requires.io/github/Ligh7bringer/Chatbot/requirements.svg?branch=dev)](https://requires.io/github/Ligh7bringer/Chatbot/requirements/?branch=dev)|[![Maintainability](https://api.codeclimate.com/v1/badges/b1106d6c1e2f197d07ba/maintainability)](https://codeclimate.com/github/Ligh7bringer/Chatbot/maintainability)|

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
* `` flask crawl `` - collects data from StackOverflow which can be later used for training the bot (stored in **chatbot/training_data/**). Command line arguments are:
  * ``--threads <number of threads to be used>``
  * ``--pages <number of pages to be crawled by each thread>``
  * ``--verbose <True/False>``
* `` flask clean `` - deletes the data collected with `` flask crawl `` (stored in **chatbot/training_data/**)
* `` flask train `` - requires data collected from the above command and tains the chatbot using it
* `` flask del_db `` - **deletes** the database generated after training the chatbot
* `` flask run `` - runs a local server. The website can be accessed at **127.0.0.1:5000**
