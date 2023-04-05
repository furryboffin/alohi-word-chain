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
            user = db.session.query(User).filter_by(email = game_data.email).first()

            # check if user exists in the db, if not create a new entry
            if user is None:
                logger.debug("user does not exist.")
                user = User(email = game_data.email)
                db.session.add(user)
            logger.debug(user)

            existing_game = db.session.query(Game).filter(Game.user_id == user.id, Game.ended_at == None).first()
            logger.debug(existing_game)
            if existing_game:
                logger.error("Cannot create a new game, existing game ongoing.")
                return {"message":"Error: Cannot create new game, an existing game is ongoing."}, 400

            # # now we create a new game
            game = Game(user_id=user.id, user_score=0.0, server_score=0.0)
            db.session.add(game)
            db.session.commit()
            return {'id': game.id},201

        except (
                ArgumentError,
                AttributeError,
                IntegrityError,
                OperationalError,
                ProgrammingError,
                sqlalchemy.exc.SQLAlchemyError,
                sqlalchemy.exc.OperationalError,
                sqlalchemy.orm.exc.NoResultFound,
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

