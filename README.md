# :zap: Honours Project 2018 - 2019 :zap:
A chatbot which can answer C++ questions based on data collected from [Stack Overflow](https://stackoverflow.com/questions/tagged/c%2b%2b?sort=votes&pageSize=15).

# Demo

There is a live demo of the project at [https://ligh7bringer.pythonanywhere.com/](https://ligh7bringer.pythonanywhere.com/).

# Repo Status
| **Branch**      | **CI**                                                       | **Code coverage**                                            | **Requirements**                                             | **Maintainability**                                          |
|-----------------|---|---|---|---|
| master |[![Build Status](https://travis-ci.org/Ligh7bringer/Chatbot.svg?branch=master)](https://travis-ci.org/Ligh7bringer/Chatbot)|[![Code Coverage](https://codecov.io/github/Ligh7bringer/Chatbot/branch/master/graphs/badge.svg)](https://codecov.io/github/Ligh7bringer/Chatbot)|[![Requirements Status](https://requires.io/github/Ligh7bringer/Chatbot/requirements.svg?branch=master)](https://requires.io/github/Ligh7bringer/Chatbot/requirements/?branch=master)|[![Maintainability](https://api.codeclimate.com/v1/badges/b1106d6c1e2f197d07ba/maintainability)](https://codeclimate.com/github/Ligh7bringer/Chatbot/maintainability)|
| development |[![Build Status](https://travis-ci.org/Ligh7bringer/Chatbot.svg?branch=dev)](https://travis-ci.org/Ligh7bringer/Chatbot)|[![Code Coverage](https://codecov.io/github/Ligh7bringer/Chatbot/branch/dev/graphs/badge.svg)](https://codecov.io/github/Ligh7bringer/Chatbot)|[![Requirements Status](https://requires.io/github/Ligh7bringer/Chatbot/requirements.svg?branch=dev)](https://requires.io/github/Ligh7bringer/Chatbot/requirements/?branch=dev)|[![Maintainability](https://api.codeclimate.com/v1/badges/b1106d6c1e2f197d07ba/maintainability)](https://codeclimate.com/github/Ligh7bringer/Chatbot/maintainability)|

# Prerequisites
* Python 3.6 or newer
* pip

# Setup
1. Clone this repo and `` cd Chatbot/ ``
2. ``pip install -r requirements.txt``
    (you may want to create a [virtual environment](https://docs.python.org/3/tutorial/venv.html) before running this command)
3. Environment variables required by Flask are set automatically (thanks to **.flaskenv**)

# Commands
After installing the required libraries, your options are:



- ```flask --help``` - shows the available commands
- ```flask crawl ``` - collects data from Stack Overflow which can be later used for training the bot (stored in **chatbot/training_data/**). Optional command line arguments are:
  - ``-t, --threads <number of threads to be used>``	
  - ``-p, --pages <number of pages to be crawled by each thread>``
  - ``-v, --verbose`` - verbose command line output
- `` flask clean `` - **deletes** the data collected with `` flask crawl `` (stored in **chatbot/training_data/**)
  * ```-y, --yes``` - don't ask for confirmation
- `` flask train `` - requires data collected from the ``crawl `` command and trains the chatbot using it
- ``` flask del_db ``` - **deletes** the database generated after training the chatbot
  * ```-y, --yes``` - don't ask for confirmation
- `` flask run `` - runs a local server. The website can be accessed at **127.0.0.1:5000**

# Tests

Unit tests can be run from the root folder of the project with the command ``pytest`` *after* installing the dependencies.