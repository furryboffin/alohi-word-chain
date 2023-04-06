from argparse import ArgumentError
from sqlite3 import IntegrityError, OperationalError, ProgrammingError
from sqlalchemy.exc import SQLAlchemyError, OperationalError, NoResultFound
from flask_restful import Resource
from flask import request
import logging as logger
from data.input import NewWordData
from model.user import User
from model.game import Game
from model.gameHistory import GameHistory
from app import db
from datetime import datetime, timedelta
from utils.helpers import generate_random_word, calculate_score, generate_result, english_words

class Word(Resource):
    def post(self):
        try:
            logger.debug("POST Method Word")
            data = request.json
            word_data = NewWordData(**data)
            user_word = word_data.word.lower()


            user = db.session.query(User).filter_by(email = word_data.email).first()
            if not user:
                return {"message":"ERROR: No user for this email exists."}

            game = db.session.query(Game).filter(Game.id == word_data.game_id, Game.ended_at == None).first()
            logger.debug(game)

            if not game:
                return {"message":"ERROR: No game for this user ongoing."}

            two_minutes_ago = datetime.utcnow() - timedelta(minutes=2)
            fifteen_seconds_ago = datetime.utcnow() - timedelta(seconds=15)

            # Next check that the word has not already been used
            # get the history of this game
            history = db.session.query(GameHistory).filter(GameHistory.user_id == user.id, GameHistory.game_id == word_data.game_id).order_by(db.desc(GameHistory.created_at)).all()
            all_words = [obj.word for obj in history]
            logger.debug(all_words)

            last_word = db.session.query(GameHistory).filter(GameHistory.user_id == user.id, GameHistory.game_id == word_data.game_id).order_by(db.desc(GameHistory.created_at)).first()

            # First check that the timeout has not passed or that this is the first word
            if last_word is not None and last_word.created_at < two_minutes_ago :
                # if we timeout, we must end the game
                game.ended_at = datetime.utcnow()
                db.session.commit()
                return {
                    "message":"TIMEOUT you took longer than 2 minutes to respond.",
                    "result":generate_result(game)
                }

            fast_bonus = True if last_word is not None and last_word.created_at > fifteen_seconds_ago else False
            # Next check that the first letter matches previous word last letter
            if last_word is not None:
                prev_last_letter = last_word.word[-1]
                if user_word[0] != prev_last_letter:
                    return {"message":"ERROR: First letter does not match last letter of previous word. Try Again!"}



            if (user_word in all_words):
                return {"message":"ERROR: this word has already been used."}

            # Next check that the word is valid
            if user_word not in english_words:
                return {"message":"ERROR: this is not a valid english word."}

            # Calculate the score
            user_score = calculate_score(word=user_word, fast_bonus=fast_bonus)

            # Store the word in the GameHistory table
            history_entry = GameHistory(game_id = word_data.game_id, user_id = 1, word=user_word, is_user=True, score=user_score)
            game.user_score += user_score

            db.session.add(history_entry)
            db.session.commit()

            all_words.append(user_word)

            last_letter = user_word[-1]

            logger.debug(word_data)
            logger.debug(last_letter)

            # create a new word based off the last letter as the first letter for the new word
            new_word = generate_random_word(last_letter, previous_words=all_words)

            # Calculate the score
            server_score = calculate_score(word=new_word, fast_bonus=False)
            game.server_score += server_score

            # store this new word in the game history table.
            history_entry = GameHistory(game_id = word_data.game_id, user_id = 1, word=new_word, is_user=False, score=server_score)
            db.session.add(history_entry)
            db.session.commit()

            logger.debug(new_word)
            return {"word":new_word},200
        except (
                ArgumentError,
                AttributeError,
                IntegrityError,
                OperationalError,
                ProgrammingError,
                SQLAlchemyError,
                OperationalError,
                NoResultFound,
                TypeError,
                KeyError,
                ValueError
            ) as e:
            logger.error(e)
            # Noramlly we'd spend more time on handling errors and providing useful
            # logs and messages for the client. I would handle errors and create codes
            # for specific known error types. due to time constraints I will just send
            # a generic error code for now
            return {"error":{"code":"generic_code_to_be_specified", "message":e.args[0]}}, 400
        except:
            logger.error("Failed inside post method of game.")
            return {"message":"Error in POST to api/v1.0/game"}, 500


