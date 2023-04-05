from flask import Flask, render_template, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
# from model.user import User
# import asyncio

import logging as logger
logger.basicConfig(level="DEBUG")

# init Flask App
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alohi-word-chain2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

user = [{"id":1, "email":"furryboffin@gmail.com"}]
gameHistory = []
game = []

# flask-server Routes
@app.route('/') # '/' for home page
def home():
    return render_template('index.html')


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     firstname = db.Column(db.String(80), nullable=False)
#     lastname = db.Column(db.String(80), nullable=False)
#     email = db.Column(db.String(80), nullable=False)

#     def __repr__(self):
#         return f"{self.id} - {self.firstname} - {self.lastname}"


# run server
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # temp_user = User(firstname="Jonathan", lastname="Fulcher", email="furryboffin@gmail.com")
        # db.session.add(temp_user)
        # db.session.commit()
        # row = db.session.query(User).filter_by(id=6).first()
        # db.session.delete(row)
        # db.session.commit()
        # logger.debug(User.query.all())
        # logger.debug(Employee.query.all())
    logger.debug("Starting the application")
    from api import *
    app.run(host="0.0.0.0", port=5000,  debug=True, use_reloader=True) # Debug true for showing errors.
