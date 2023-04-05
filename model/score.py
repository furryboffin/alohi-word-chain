from app import db
import logging as logger

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer)
    def __repr__(self):
        logger.debug("in repr of Game")
        return f"{self.id}"
