from click import DateTime
from flask_restful import Resource
from flask import request, jsonify
import logging as logger
from data.input import NewWordData
import random
from model.user import User
import nltk
from model.gameHistory import GameHistory
from app import app, db
from datetime import datetime, timedelta


# Install NLTK's corpus data
# nltk.download('words')

from nltk.corpus import words
english_words = set(words.words())

def generate_random_word(starting_letter):
    # Try 5 times to find a good word
    word = ""
    score = 0
    count = 5 #we could make a difficulty level and use that.
    while True:
        new_word = random.choice(list(english_words))
        if count > 0 and new_word.startswith(starting_letter):
            if word == "" or score < calculate_score(new_word):
                word = new_word
                count -= 1
        elif count == 0:
            return word


def calculate_score(word):
    score = 0
    for char in word:
        if char in 'aeiou':
            score += 2
        elif char.isalpha():
            score += 1
    return score

class Word(Resource):

    def get(self):
        logger.debug("GET Method")
        return {"message":"Inside GET Method"},200

    def post(self):
        logger.debug("POST Method Word")
        # logger.debug(self.dispatch_request.)
        data = request.json
        logger.debug("POST Method body : {}".format(data))
        wordData = NewWordData(**data)
        user_word = wordData.word.lower()

        user = db.session.query(User).filter_by(email = wordData.email).first()
        if not isinstance(user, User):
            return {"message":"ERROR: No game for this user is ongoing."}

        two_minutes_ago = datetime.utcnow() - timedelta(minutes=2)

        last_word = db.session.query(GameHistory).filter_by(GameHistory.created_at > two_minutes_ago, user_id = user.id).order_by(db.desc(GameHistory.created_at)).first()

        # First check that the timeout has not passed
        if last_word is None:
            return {"message":"ERROR: TIMEOUT you took longer than 2 minutes to respond."}

        # Next check that the word is valid
        if user_word not in english_words:
            return {"message":"ERROR: this is not a valid english word."}

        # Next check that the word has not already been used
        # get the history of this game
        all_words = db.session.query(GameHistory).filter_by(user_id = user.id).order_by(db.desc(GameHistory.created_at)).all()
        if (user_word in all_words):
            return {"message":"ERROR: this word has already been used."}

        # Calculate the score
        user_score = calculate_score(user_word)

        # Store the word in the GameHistory table
        with app.app_context():
            history_entry = GameHistory(game_id = wordData.game_id, user_id = 1, word=user_word, is_user=True, score=user_score)
            db.session.add(history_entry)
            db.session.commit()

        last_letter = user_word[-1]

        logger.debug(wordData)
        logger.debug(last_letter)

        # create a new word based off the last letter as the first letter for the new word
        new_word = generate_random_word(last_letter)

         # Calculate the score
        server_score = calculate_score(new_word)

        # store this new word in the game history table.
        with app.app_context():
            history_entry = GameHistory(game_id = wordData.game_id, user_id = 1, word=new_word, is_user=False, score=server_score)
            db.session.add(history_entry)
            db.session.commit()

        logger.debug(new_word)
        return {"word":new_word},200


