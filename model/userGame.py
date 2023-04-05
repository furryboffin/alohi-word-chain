from app import db

class UserGame(db.Model):
    game_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"{self.game_id} - {self.user_id}"
