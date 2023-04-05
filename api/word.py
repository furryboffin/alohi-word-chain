from click import DateTime
from flask_restful import Resource
from flask import request, jsonify
import logging as logger
from data.input import NewWordData
import random
from model.user import User
from model.game import Game
from model.gameHistory import GameHistory
from app import app, db
from datetime import datetime, timedelta
import nltk

# Install NLTK's corpus data
# nltk.download('words')
from nltk.corpus import words
english_words = set(words.words())

#JRF TODO:
# 1. add the endpoint to get history
# 2. add the score output at end of game
# 3. add readme to repo with explanation of the status of this project and what can be done to improve

#JRF TODO, add failure handling... we should pass in the list of words in the history
# so that they can be checked against the result... if we cannot get a word that is not
# already in the list then we timeout and return an empty word.
# if this function returns an empty word then the server causes the game to end with the
# timeout. This code has yet to be added.
def generate_random_word(starting_letter):
    # Try 5 times to find a good word
    word = ""
    score = 0
    timeout = 10000
    count = 5 #we could make a difficulty level and use that.
    while True:
        timeout-=1
        new_word = random.choice(list(english_words))
        if count > 0 and timeout and new_word.startswith(starting_letter):
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
        data = request.json
        wordData = NewWordData(**data)
        user_word = wordData.word.lower()


        user = db.session.query(User).filter_by(email = wordData.email).first()
        if not user:
            return {"message":"ERROR: No user for this email exists."}

        game = db.session.query(Game).filter(Game.id == wordData.game_id, Game.ended_at == None).first()
        logger.debug(game)

        if not game:
            return {"message":"ERROR: No game for this user ongoing."}

        two_minutes_ago = datetime.utcnow() - timedelta(minutes=2)

        last_word = db.session.query(GameHistory).filter(GameHistory.user_id == user.id, GameHistory.game_id == wordData.game_id).order_by(db.desc(GameHistory.created_at)).first()

        # First check that the timeout has not passed or that this is the first word
        if last_word is not None and last_word.created_at < two_minutes_ago :
            # if we timeout, we must end the game
            game.ended_at = datetime.utcnow()
            db.session.commit()
            return {"message":"ERROR: TIMEOUT you took longer than 2 minutes to respond."}

        # Next check that the first letter matches previous word last letter
        if last_word is not None:
            prev_last_letter = last_word.word[-1]
            if user_word[0] != prev_last_letter:
                return {"message":"ERROR: First letter does not match last letter of previous word. Try Again!"}



        # Next check that the word has not already been used
        # get the history of this game
        history = db.session.query(GameHistory).filter(GameHistory.user_id == user.id, GameHistory.game_id == wordData.game_id).order_by(db.desc(GameHistory.created_at)).all()
        all_words = [obj.word for obj in history]
        logger.debug(all_words)
        if (user_word in all_words):
            return {"message":"ERROR: this word has already been used."}

        # Next check that the word is valid
        if user_word not in english_words:
            return {"message":"ERROR: this is not a valid english word."}

        # Calculate the score
        # JRF TODO, add handling for extra score if guess was faster than 15 seconds
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


