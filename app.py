# -*- coding: utf-8 -*-

from flask import Flask, render_template
import requests as req

app = Flask(__name__)

# attribs = ["style=text-decoration:none;" for i in range(3)]
# words = set([f'nothing {i+1}' for i in range(3)])
words = []


def rand_word():
    r = req.get('http://free-generator.ru/generator.php?action=word&type=1')
    return r.json()["word"]["word"]


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/set_words/<ws>')
def set_words(ws):
    global words
    words = ws[1:-1].replace('\'', '').split(', ')
    return ''.join(words)


@app.route('/get_words/<id>')
def get_words(id):
    id = int(id)
    global words
    if id <= len(words)-1:
        return words[id]
    else:
        return ""


if __name__ == "__main__":
    app.run(debug=True)
