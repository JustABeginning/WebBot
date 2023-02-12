"""Python-Javascript Inter-Communication"""

# Import Modules

import logging
import os
import codecs
import re
import asyncio
from datetime import datetime
import openai

from flask import Flask, request
from flask import make_response
from flask_cors import CORS

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

completion = openai.Completion()

# Global Tokens

OPENAI_TOKEN = "OPENAI_API_KEY"

# OpenAI API key
aienv = os.getenv('OPENAI_KEY')
if aienv is None:
    openai.api_key = OPENAI_TOKEN
else:
    openai.api_key = aienv
print(aienv)

# Lots of console output
DEBUG = True

# User Session timeout
TIMSTART = 300
TIM = 1

# Defaults
USER = "username"
RUNNING = False
CACHE = None
QCACHE = None
CHAT_LOG = None
BOTNAME = 'bot'
USERNAME = 'user'
# Max chat log length (A token is about 4 letters and max tokens is 2048)
MAX = int(3000)


################
# Main functions #
################


def limit(text):
    if (len(text) >= MAX):
        inv = MAX * 10
        print("Reducing length of chat history... This can be a bit buggy.")
        nl = text[inv:]
        text = re.search(r'(?<=\n)[\s\S]*', nl).group(0)  # type: ignore
        return text
    else:
        return text


def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = 'The following is a chat between two users:\n\n'
    chat_log = limit(chat_log)
    now = datetime.now()
    ampm = now.strftime("%I:%M %p")
    t = '[' + ampm + '] '
    return f'{chat_log}{t}{USERNAME}: {question}\n{t}{BOTNAME}: {answer}\n'


def ask(question, chat_log=None):
    if chat_log is None:
        chat_log = 'The following is a chat between two users:\n\n'
    now = datetime.now()
    ampm = now.strftime("%I:%M %p")
    t = '[' + ampm + '] '
    prompt = f'{chat_log}{t}{USERNAME}: {question}\n{t}{BOTNAME}:'
    response = completion.create(prompt=prompt, engine="text-davinci-003",
                                 temperature=0.5, frequency_penalty=0.5,
                                 presence_penalty=0.5, best_of=3, max_tokens=500)
    answer = response.choices[0].text.strip()  # type: ignore
    return answer
    # fp = 15 pp= 1 top_p = 1 temp = 0.9


async def interact(text, new):
    global CHAT_LOG
    global CACHE
    global QCACHE
    print("\n==========START==========\n")
    if new is True:
        if DEBUG is True:
            print("Chat_Log CACHE is...")
            print(CACHE)
            print("Question CACHE is...")
            print(QCACHE)
        CHAT_LOG = CACHE
        question = QCACHE
    else:
        question = text
        QCACHE = question
        CACHE = CHAT_LOG
    try:
        answer = ask(question, CHAT_LOG)
        if DEBUG is True:
            print("Input :\n" + question)  # type: ignore
            print("\nOutput :\n" + answer)  # type: ignore
            print("\n====================\n")
        CHAT_LOG = append_interaction_to_chat_log(
            question, answer, CHAT_LOG)  # type: ignore
        if DEBUG is True:
            # Print the chat log for debugging
            print('-----PRINTING CHAT LOG-----\n')
            print(CHAT_LOG)
            print('-----END CHAT LOG-----\n')
    except Exception as e:
        answer = str(e)
        print('\nException ::\n' + answer)
    return answer


def interact_call(update, new):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    answer = loop.run_until_complete(interact(update, new))
    return answer

# Python Web


app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    with codecs.open("app_index.html", "r") as f:
        return f.read()


@app.route("/index")
@app.route('/login', methods=['GET', 'POST'])  # type: ignore
def login():
    if request.method == 'POST':
        datafromjs = request.form['mydata']
        result = interact_call(datafromjs, False)
        resp = make_response(result)
        resp.headers['Content-Type'] = "application/json"
        return resp


if __name__ == "__main__":
    app.run(debug=True)
