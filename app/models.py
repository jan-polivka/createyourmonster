from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Sheet(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    hitPoints = db.Column(db.Integer)
    name = db.Column(db.String(64))
    gender = db.Column(db.String(64))
    level = db.Column(db.Integer)
    #Here is a limitation of SQL
    #I can't add any homebrew because the choices are hardcoded.
    #I think I need Entry-Attribute-Value solution and NoSQL
    #seems much better suited for this
    bard = db.Column(db.Integer)
    barbarian = db.Column(db.Integer)
    common = db.Column(db.Boolean)
    elvish = db.Column(db.Boolean)
    dwarvish = db.Column(db.Boolean)
    acrobatics = db.Column(db.Integer)
    animals = db.Column(db.Integer)
    arcana = db.Column(db.Integer)
    

    def __repr__(self):
        return '<Character {}>'.format(self.name)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(64),  index = True, unique = True)
    password_hash = db.Column(db.String(128))
    sheets = db.relationship('Sheet', backref = 'author', lazy = 'dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
