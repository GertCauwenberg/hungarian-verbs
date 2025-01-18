#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright 2025 Gert Cauwenberg
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import random
import sqlite3


class Database:
    def __init__(self):
        self.con = sqlite3.connect("verbs.db")
        self.cur = self.con.cursor()

    def close(self):
        self.con.commit()
        self.con.close()

    def get_language(self, lang):
        res = self.cur.execute("SELECT id from languages where language = ?", (lang,))
        (lid,) = res.fetchone()
        return lid

    def get_tense(self, tense, lang=None):
        if isinstance(lang, str):
            lang = self.get_language(lang)
        res = self.cur.execute(
            "SELECT tense from tense_translations where language = ? and translation = ?",
            (lang, tense))
        (tid,) = res.fetchone()
        return tid

    def get_tenses(self, lang):
        if isinstance(lang, str):
            lang = self.get_language(lang)
        res = self.cur.execute(
            "SELECT tense, translation from tense_translations where language = ?",
            (lang, ))
        ids = res.fetchall()
        return ids

    def get_verbs(self, tense, lang):
        if isinstance(lang, str):
            lang = self.get_language(lang)
        res = self.cur.execute(
            "SELECT határozatlan, határozott, translation from verbs, verb_translations "
            "where tense=? and verbs.id = verb_translations.verb and language=?",
            (tense, lang))
        return res.fetchall()


def select_from_dict(options, name):
    index = 0
    print('Select a ' + name + ':')
    for optionName in options:
        index = index + 1
        print(str(index) + ') ' + optionName[1])
    selected = None
    while not selected:
        rawinput = input(name + ': ')
        try:
            inputnbr = int(rawinput) - 1
        except ValueError:
            inputnbr = -1
        if -1 < inputnbr < len(options):
            selected = options[inputnbr]
            print('Selected ' + name + ': ' + selected[1])
        else:
            print('Please select a valid ' + name + ' number')
    return selected


def ask_question(question, answer, t=None):
    if t:
        rawinput = input(f"{question} ({t}): ")
    else:
        rawinput = input(question + ': ')
    if rawinput.lower() == answer.lower():
        corr = 1
    else:
        print(f"Not correct, the answer is {answer}")
        corr = 0
    return corr


def exercise(nbr, verbs, direction):
    score = 0
    for ex in range(nbr):
        verb = random.choice(verbs)
        if direction == 3:
            d = random.randrange(2) + 1
        else:
            d = direction
   
        types = ['indef', 'def']
        if verb[1]:
            t = random.randrange(2)
        else:
            t = 0

        if d == 1:
            score += ask_question(verb[2], verb[t], types[t])
        else:
            score += ask_question(verb[t], verb[2])
    return score


if __name__ == "__main__":
    db = Database()
    tenses = db.get_tenses("english")
    choice = select_from_dict(tenses, "tense")
    while True:
        inputRaw = input("How many exercises do you want (1-100)? ")
        try:
            inputNo = int(inputRaw)
        except ValueError:
            inputNo = 0
        if inputNo < 1 or inputNo > 100:
            print("Please select a valid number (1-100)")
        else:
            break

    direction = select_from_dict([(1, "eng -> hun"), (2, "hun -> eng"), (3, "both")], "direction")

    verbs = db.get_verbs(choice[0], 1)
    score = exercise(inputNo, verbs, direction[0])

    print(f"You had {score} out of {inputNo} correct, {100.0*score/inputNo:.0f} %")
