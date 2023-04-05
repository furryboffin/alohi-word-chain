from flask_restful import Resource
from flask import request, jsonify
import logging as logger
from data.input import GameId

class EndGame(Resource):

    def post(self):
        logger.debug("POST Method EndGame")
        data = request.json
        logger.debug("POST Method body : {}".format(data))
        game_id = GameId(**data)

        logger.debug(game_id)

        # END the Game.
        # First check that the game is started and has not already ended.

        if None:
            return {"message": "ERROR: game is not started."}

        if None:
            return {"message": "ERROR: game has already ended."}



        return {"scores":{"user":10, "server": 20, "winner": "server"}},200



