from argparse import ArgumentError
from sqlite3 import IntegrityError, OperationalError, ProgrammingError
from flask import request, jsonify
from flask_restful import Resource
import logging as logger
from model.game import Game
from model.user import User
from app import app, db
from data.input import NewGameData

class Game(Resource):
    def get(self):
        try:
            # logger.debug("GET Method of GameId taskID= {}".format(gameId))
            # return {"message":"Inside GET Method of TaskByID", "id":int(gameId)},200
            logger.debug("GET Method")
            return {"message":"Inside GET Method"},200
        except ValueError:
            logger.error("failed to parse int.")
            return {"message":"Error in GET Method of TaskByID, failed to parse ID, it should be an integer."},400
        except:
            logger.error("failed to parse int with some uknown error.")
            return {"message":"Internal Server Error in GET Method of TaskByID."},500

    def post(self):
        # with app.app_context():
        try:
            # JRF TODO, add validation for json requests
            data = request.json
            logger.debug("POST Method body : {}".format(data))
            new_game = NewGameData(**data)
            logger.debug(new_game)
            # row = db.session.query(User).filter_by(id=4).first()
            # if isinstance(row, User):
            #     db.session.delete(row)
            #     db.session.commit()
            user = db.session.query(User).filter_by(email = new_game.email).first()
            logger.debug(User.query.all())
            # check if user exists in the db, if not create them
            if not isinstance(user, User):
                with app.app_context():
                    logger.debug("user does not exist.")
                    user = User(firstname = "Not",lastname = "Used", email = new_game.email)
                    db.session.add(user)
                    db.session.commit()


            # # # now we create a new game
            try:
                # game = Game(theme = "test")
                with app.app_context():
                    game = Game(user_score=0, server_score=0)
                    logger.debug("About to save game")
                    db.session.add(game)
                    # # db.session.flush()
                    db.session.commit()
                    # new_id = game.id
                    # logger.debug("ID:")
                    # logger.debug(id)
            except ArgumentError:
                logger.debug("ArgumentError")
            except AttributeError:
                logger.debug("AttributeError")
            except IntegrityError:
                logger.debug("IntegrityError")
            except OperationalError:
                logger.debug("OperationalError")
            except ProgrammingError:
                logger.debug("ProgrammingError")
            except ValueError:
                logger.debug("ValueError")
            except TypeError:
                logger.debug("TypeError")
            except:
                logger.debug("unknown error")
                # if not isinstance(game, Game):
                #     logger.debug("NOT GAME")
                # logger.debug(game)
            # logger.debug(f"{result}")

            # logger.debug(game.id)
            return {'id': 1},200 #game.id}, 200


        except:
            logger.error("Failed inside post method of game.")
            return {"message":"Error in POST to api/v1.0/game"}

    # def put(self):
    #     logger.debug("PUT Method of TaskByID")
    #     return {"message":"Inside PUT Method of TaskByID"},200

    # def delete(self):
    #     logger.debug("DELETE Method of TaskByID")
    #     return {"message":"Inside DELETE Method of TaskByID"},200


