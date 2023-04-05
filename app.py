from flask import Flask, render_template, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import asyncio

import logging as logger
logger.basicConfig(level="DEBUG")

# init Flask App
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# flask-server Routes
@app.route('/') # '/' for home page
def home():
    return render_template('index.html')

async def sleep(s):
    return await asyncio.sleep(s, result='hello')

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    firstname = db.Column(db.String(80), nullable=False)
    salary = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"{self.firstname} - {self.lastname} - {self.gender} - {self.salary}"

# run server
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(logger.debug(sleep(10)))
    # logger.debug(sleep(10))
    with app.app_context():
        # db.create_all()
        # emp = Employee(firstname="James", lastname="Bond", gender="Male", salary=100000)
        # db.session.add(emp)
        # db.session.commit()
        logger.debug(Employee.query.all())
    logger.debug("Starting the application")
    from api import *
    app.run(host="0.0.0.0", port=5000,  debug=True, use_reloader=True) # Debug true for showing errors.
