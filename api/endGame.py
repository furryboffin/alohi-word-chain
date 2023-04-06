from datetime import datetime
from flask_restful import Resource
from argparse import ArgumentError
from sqlite3 import IntegrityError, OperationalError, ProgrammingError
from sqlalchemy.exc import SQLAlchemyError, OperationalError, NoResultFound
from flask import request
import logging as logger
from data.input import EndGameData
from model.game import Game
from model.user import User
from utils.helpers import generate_result
from app import db

class EndGame(Resource):

    def post(self):
        try:
            logger.debug("POST Method EndGame")
            data = request.json
            logger.debug("POST Method body : {}".format(data))
            end_game_data = EndGameData(**data)

            logger.debug(end_game_data)
            user = db.session.query(User).filter_by(email = end_game_data.email).first()
            if not user:
                return {"message":"ERROR: No user for this email exists."}
            logger.debug(user)
            game = db.session.query(Game).filter(Game.user_id == user.id, Game.id == end_game_data.game_id, Game.ended_at == None).first()
            logger.debug(game)

            # First check that the game is started and has not already ended.
            if not game:
                logger.debug("NOT GAME TRUE")
                return {"message":"ERROR: No game for this user ongoing."}
            logger.debug("GAME ongoing")
            # END the Game.
            game.ended_at = datetime.utcnow()
            db.session.commit()

            # history = db.session.query(GameHistory).filter(GameHistory.user_id == user.id, GameHistory.game_id == end_game_data.game_id).order_by(db.desc(GameHistory.created_at)).all()
            result = generate_result(game)
            return result

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



