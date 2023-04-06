from flask_restful import Resource
from argparse import ArgumentError
from sqlite3 import IntegrityError, OperationalError, ProgrammingError
from sqlalchemy.exc import SQLAlchemyError, OperationalError, NoResultFound
from flask import request
import logging as logger
from data.input import GameHistoryData
from model.game import Game
from model.gameHistory import GameHistory as GameHistoryModel
from model.user import User
from app import db

class GameHistory(Resource):

    def get(self):
        try:
            logger.debug("GET Method GameHistory")
            data = request.json
            logger.debug("POST Method body : {}".format(data))
            game_history_data = GameHistoryData(**data)

            logger.debug(game_history_data)

            user = db.session.query(User).filter_by(email = game_history_data.email).first()
            if not user:
                return {"message":"ERROR: No user for this email exists."}
            logger.debug(user)

            game = db.session.query(Game).filter(Game.id == game_history_data.game_id, Game.user_id == user.id).first()
            logger.debug(game)

            # First check that the game exists.
            if not game:
                return {"message":"ERROR: No game for this user by that game_id."}
            logger.debug("DEBUG 1")
            history = db.session.query(GameHistoryModel).filter(GameHistoryModel.user_id == user.id, GameHistoryModel.game_id == game_history_data.game_id).order_by(db.desc(GameHistoryModel.created_at)).all()
            # convert GameHistory objects to list of dictionaries
            game_history_dicts = []
            for game_history in history:
                game_history_dicts.append({
                    'word': game_history.word,
                    'player_name': 'user' if game_history.is_user else 'server',
                    'score': game_history.score,
                    'created_at': game_history.created_at.strftime('%Y-%m-%d %H:%M:%S')
                })
            logger.debug("DEBUG 2")
            logger.debug(game_history_dicts)
            return game_history_dicts

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



