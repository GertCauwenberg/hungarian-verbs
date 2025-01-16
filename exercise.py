
import sys
import random
import re
import sqlite3

class Database:
    def __init__(self):
        self.con = sqlite3.connect("verbs.db")
        self.cur = self.con.cursor()

    def close(self):
        self.con.commit()
        self.con.close()

    def getLanguage(self, lang):
        res = self.cur.execute("SELECT id from languages where language = ?", (lang,))
        (id,) = res.fetchone()
        return id

    def getTense(self, tense, lang=None):
        if isinstance(lang, str):
           lang = self.getLanguage(lang)
        res = self.cur.execute("SELECT tense from tense_translations where language = ? and translation = ?", (lang, tense))
        (id,) = res.fetchone()
        return id

    def getTenses(self, lang):
        if isinstance(lang, str):
           lang = self.getLanguage(lang)
        res = self.cur.execute("SELECT tense, translation from tense_translations where language = ?", (lang, ))
        ids = res.fetchall()
        return ids

    def getVerbs(self, tense, lang):
        if isinstance(lang, str):
           lang = self.getLanguage(lang)
        res = self.cur.execute("SELECT határozatlan, határozott, translation from verbs, verb_translations where tense=? and verbs.id = verb_translations.verb and language=?", (tense, lang))
        return res.fetchall()


def selectFromDict(options, name):
    index = 0
    print('Select a ' + name + ':')
    for optionName in options:
        index = index + 1
        print(str(index) + ') ' + optionName[1])
    inputValid = False
    while not inputValid:
        inputRaw = input(name + ': ')
        try:
            inputNo = int(inputRaw) - 1
        except ValueError:
            inputNo = -1
        if inputNo > -1 and inputNo < len(options):
            selected = options[inputNo]
            print('Selected ' +  name + ': ' + selected[1])
            inputValid = True
            break
        else:
            print('Please select a valid ' + name + ' number')
    return selected

def askQuestion(question, answer, t=None):
    if t:
       inputRaw = input(f"{question} ({t}): ")
    else:
       inputRaw = input(question + ': ')
    if inputRaw.lower() == answer.lower():
       score = 1
    else:
       print(f"Not correct, the answer is {answer}")
       score = 0
    return score

def exercise(nbr, verbs, direction):
   score = 0
   for ex in range(nbr):
      verb = random.choice(verbs)
      if direction == 3:
         d = random.randrange(2) + 1
      else:
         d = direction
   
      types = [ 'indef', 'def' ]
      if verb[1]:
         t = random.randrange(2)
      else:
         t = 0

      if d == 1:
         score += askQuestion(verb[2], verb[t], types[t])
      else:
         score += askQuestion(verb[t], verb[2])
   return score


if __name__ == "__main__":
   db = Database()
   tenses = db.getTenses("english")
   choice = selectFromDict(tenses, "tense")
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

   direction = selectFromDict([ (1,"eng -> hun"), (2, "hun -> eng"), (3, "both") ], "direction")

   verbs = db.getVerbs(choice[0], 1)
   score = exercise(inputNo, verbs, direction[0])

   print(f"You had {score} out of {inputNo} correct, {100.0*score/inputNo} %")
