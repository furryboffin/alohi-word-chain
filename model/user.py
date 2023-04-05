from db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    def __repr__(self):
        return f"id: {self.id}, email: {self.email}"

