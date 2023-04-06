from flask import jsonify, make_response
from flask_restful import Api
from app import app
from .gameHistory import GameHistory
from .newGame import NewGame
from .word import Word
from .endGame import EndGame

restServer = Api(app)

@app.errorhandler(404)
def handle_404_error(_error):
    return {'error': {'code':'not_found', 'message':'The requested resource does not exist.'}}

restServer.add_resource(NewGame, "/api/v1.0/game/new",)
restServer.add_resource(EndGame, "/api/v1.0/game/end",)
restServer.add_resource(Word, "/api/v1.0/game/word",)
restServer.add_resource(GameHistory, "/api/v1.0/game/history",)
