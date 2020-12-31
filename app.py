# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect
import requests as req

app = Flask(__name__)

attribs = ["style=text-decoration:none;" for i in range(3)]
words = set([f'nothing {i+1}' for i in range(3)])


def rand_word():
    r = req.get('http://free-generator.ru/generator.php?action=word&type=1')
    return r.json()["word"]["word"]


@app.route('/<new>')
@app.route('/index/<new>')
def index(new=None):
    if new == 'new':
        global attribs
        attribs = ["style=text-decoration:none;" for i in range(3)]
        global words
        while True:
            words = set([rand_word() for i in range(3)])
            if len(words) == 3:
                break
    if new in ['0', '1', '2']:
        attribs[int(new)] = "style=display:none;"
        '''
        if attribs.count("style=display:none;") == 3:
            return redirect("/index/new")
        '''
    return render_template('index.html', words=list(words), attribs=attribs)


if __name__ == "__main__":
    app.run(debug=True)