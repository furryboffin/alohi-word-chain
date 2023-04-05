from flask import Flask, render_template, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from db import db

import logging as logger
logger.basicConfig(level="DEBUG")

# init Flask App
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alohi-word-chain2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)  # call init_app here rather than initialising db here
from model.user import User
from model.game import Game
from model.gameHistory import GameHistory

# run server
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        logger.debug(User.query.all())
    logger.debug("Starting the application")
    from api import *
    app.run(host="0.0.0.0", port=5000,  debug=True, use_reloader=True) # Debug true for showing errors.
