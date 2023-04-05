from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from model.user import User
# import flask_migrate

import logging as logger
logger.basicConfig(level="DEBUG")

# init Flask App
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///word-chain.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# run server
if __name__ == "__main__":
    # from model.game import Game
    # from model.userGame import UserGame
    # from model.gameHistory import GameHistory

    with app.app_context():
        # db.create_all()
        user = User(firstname="Jonathan", lastname="Fulcher", email="furryboffin@gmail.com")
        # game = Game(theme="Fun")
        # game = UserGame(game_id=1, user_id=1)
        # game = Game(theme="Fun")
        db.session.add(user)
        db.session.commit()
        logger.debug(User.query.all())

    logger.debug("Starting the application")
    from api import *
    app.run(host="0.0.0.0", port=5000,  debug=True, use_reloader=True) # Debug true for showing errors.




 # from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

        # engine = create_engine('sqlite:///college.db', echo = True)
        # meta = MetaData()

        # students = Table(
        #     'students', meta,
        #     Column('id', Integer, primary_key = True),
        #     Column('name', String),
        #     Column('lastname', String),
        # )
        # meta.create_all(engine)
        # logger.debug(User.query.all())
