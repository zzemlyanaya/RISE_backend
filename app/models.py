from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    type = db.Column(db.Integer, index=True, nullable=False, default=1)
    age = db.Column(db.Integer, nullable=True)
    location = db.Column(db.String(128), nullable=True)
    about = db.Column(db.Text, nullable=True)
    project = db.relationship('Project', cascade="all, delete-orphan")

    def to_json(self):
        return {'id': self.id, 'email': self.email, 'name': self.name, 'type': self.type,
                'age': self.age, 'location': self.location, 'about': self.about}

    def __init__(self, id, email, name, type, age, location, about):
        self.id = id
        self.email = email
        self.name = name
        self.type = type
        self.age = age
        self.location = location
        self.about = about


class Project(db.Model):
    __tablename__= 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    contact = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    descriptionShort = db.Column(db.String(256))
    descriptionLong = db.Column(db.Text)
    cost = db.Column(db.String(64), index=True)
    deadlines = db.Column(db.String(64), index=True)
    website = db.Column(db.String(64), nullable=True)

    def to_json(self):
        return {'id': self.id, 'name': self.name, 'contact': self.contact,
                'descriptionShort': self.descriptionShort, 'descriptionLong': self.descriptionLong,
                'cost': self.cost, 'deadlines': self.deadlines, 'website': self.website}

    def __init__(self, name, contact, descriptionShort, descriptionLong, cost, deadlines, website):
        self.contact = contact
        self.name = name
        self.descriptionShort = descriptionShort
        self.descriptionLong = descriptionLong
        self.cos = cost
        self.deadlines = deadlines
        self.website = website


class Auth(db.Model):
    __tablename__ = 'auths'
    id = db.Column(db.Integer, primary_key=True)
    passwordToken = db.Column(db.Integer)

    def __init__(self, id, passToken):
        self.id = id
        self.passwordToken = passToken


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    fromm = db.Column(db.Integer, index=True)
    to = db.Column(db.Integer, index=True)
    text = db.Column(db.String(1024), index=True)

    def to_json(self):
        return {'id': self.id, 'from': self.fromm, 'to': self.to, 'text': self.text}
