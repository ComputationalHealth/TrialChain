from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    propername = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class MultichainNode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(128), index=True, unique=True)
    connect = db.Column(db.Boolean, default=False)
    send = db.Column(db.Boolean, default=False)
    receive = db.Column(db.Boolean, default=False)
    issue = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Address {}>'.format(self.address)

class EthTx(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(128), index=True, unique=True)
    txid = db.Column(db.String(128), index=True, unique=True)
    mchash = db.Column(db.String(128), index=True)
    sent = db.Column(db.DateTime)

    def __repr__(self):
        return '<Tx ID {}>'.format(self.txid)
