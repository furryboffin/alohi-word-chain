
from db import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    ended_at = db.Column(db.DateTime, nullable=True)
    user_score = db.column(db.Float)
    server_score = db.column(db.Float)

    def __repr__(self):
        return f"id: {self.id}, user_id: {self.user_id}, created_at {self.created_at}, user_score: {self.user_score}, server_score: {self.server_score}"
