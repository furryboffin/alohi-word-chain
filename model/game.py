
from app import db
import logging as logger

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    ended_at = db.Column(db.DateTime, nullable=True)
    user_score = db.column(db.Float)
    server_score = db.column(db.Float)

    def __repr__(self):
        logger.debug("in repr of Game")
        return f"{self.id}"
