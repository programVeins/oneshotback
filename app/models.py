from app import db, login
from app.refGen import refGen
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

     
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), index=True, unique=False)
    lastname = db.Column(db.String(64), index=True, unique=False)
    torefID = db.Column(db.String(64), index=True, unique=True)
    fromrefID = db.Column(db.String(64), index=True, unique=False)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    contactnum = db.Column(db.String(64), index=True, unique=True)
    hasPaid = db.Column(db.Integer, index=True, unique=False)
    numberOfReferals = db.Column(db.Integer, index=True, unique=False)
    isAdmin = db.Column(db.Integer, index=True, unique=False)
    paynum = db.Column(db.String(64), index=True, unique=False)
    bname = db.Column(db.String(128), index=True, unique=False)
    ifsc = db.Column(db.String(64), index=True, unique=False)
    datePaid = db.Column(db.DateTime, index=True)
    
    def genRefID(self):
        self.torefID = refGen(8)

    def __repr__(self):
        return '<User {}>'.format(self.firstname)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
