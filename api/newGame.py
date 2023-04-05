from argparse import ArgumentError
import datetime
from sqlite3 import IntegrityError, OperationalError, ProgrammingError
from flask import request, jsonify
from flask_restful import Resource
import logging as logger

import sqlalchemy
from model.game import Game
from model.user import User
from app import app, db
from data.input import NewGameData

class NewGame(Resource):
    def post(self):
        # JRF TODO add global try, except with finally to complete the session.commit()
        # JRF TODO before allowing the user to create a new game, check if there is a game
        # already ongoing.

        try:
            data = request.json
            logger.debug("POST Method body : {}".format(data))
            game_data = NewGameData(**data)
            logger.debug(f"{game_data}")

            user = db.session.query(User).filter_by(email = game_data.email).first()
            logger.debug("DEBUG 3")

            # check if user exists in the db, if not create them
            if user is None:
                logger.debug("user does not exist.")
                user = User(email = game_data.email)
                db.session.add(user)
                db.session.commit()

            logger.debug(user)

            # # now we create a new game
            game = Game(user_id=user.id, user_score=0.0, server_score=0.0)
            logger.debug("About to save game")
            db.session.add(game)
            db.session.flush()
            logger.debug("About to commit game")
            db.session.commit()
            logger.debug(game)

            if not game:
                logger.debug("NOT GAME")
            logger.debug(game.id)
            return {'id': game.id},201

        except (
                ArgumentError,
                AttributeError,
                IntegrityError,
                OperationalError,
                ProgrammingError,
                sqlalchemy.exc.SQLAlchemyError,
                TypeError,
                KeyError,
                ValueError
            ) as e:
                logger.error(e)
                # Noramlly we'd spend more time on handling errors and providing useful
                # logs and messages for the client.
                return {"message":e.args[0]}, 400

        except:
            logger.error("Failed inside post method of game.")
            return {"message":"Error in POST to api/v1.0/game"}, 500
