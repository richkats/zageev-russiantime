# -*- coding: utf-8 -*-

import peewee as pw
from random import shuffle

db = pw.SqliteDatabase('words.db')


class Words(pw.Model):
    word_id = pw.PrimaryKeyField()
    russian = pw.CharField()
    english = pw.CharField()

    class Meta:
        database = db


def create_tables():
    with db:
        db.create_tables([Words])


def get_words():
    words = list(Words.select())
    shuffle(words)
    return words[:3]


def compare(guessing, words):
    for word in words:
        if word.english in guessing:
            words.remove(word)
            return word

    return False
