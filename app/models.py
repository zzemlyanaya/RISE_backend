from flask_login import UserMixin

from app import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    type = db.Column(db.Integer, index=True, nullable=False, default=1)
    age = db.Column(db.Integer, nullable=True)
    location = db.Column(db.String(128), nullable=True)
    projects = db.relationship('Project', backref='contact', lazy=True)
    about = db.Column(db.Text, nullable=True)

    def to_json(self):
        return {'id': self.id, 'email': self.email, 'name': self.name, 'type': self.type,
                'age': self.age, 'location': self.location, 'projects':self.projects, 'about':self.about}


class Project(db.Model):
    __tablename__= 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    contact = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    descriptionShort = db.Column(db.String(256))
    descriptionLong = db.Column(db.Text)
    cost = db.Column(db.String(64), index=True)
    deadlines = db.Column(db.String(64), index=True)
    website = db.Column(db.String(64), nullable=True)


class Auth(db.Model):
    __tablename__ = 'auths'
    id = db.Column(db.Integer, primary_key=True)
    passwordToken = db.Column(db.Integer)


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    fromm = db.Column(db.Integer, index=True)
    to = db.Column(db.Integer, index=True)
    text = db.Column(db.String(1024), index=True)
