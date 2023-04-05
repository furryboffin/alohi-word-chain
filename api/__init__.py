from flask_restful import Api
from app import app
from .game import Game
from .word import Word
from .endGame import EndGame

# from .taskByID import TaskByID
# from .employee import Employee

restServer = Api(app)

restServer.add_resource(Game, "/api/v1.0/game/new",)
restServer.add_resource(EndGame, "/api/v1.0/game/end",)
restServer.add_resource(Word, "/api/v1.0/game/word",)

# restServer.add_resource(TaskByID, "/api/v1.0/task")
# restServer.add_resource(employee, "/api/v1.0/employee")
