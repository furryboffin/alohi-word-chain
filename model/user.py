from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    def __repr__(self):
        return f"id: {self.id}, firstname: {self.firstname}, lastname: {self.lastname}"

