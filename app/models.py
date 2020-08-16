from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    name = db.Column(db.String(64), index=True, nullable=False)
    type = db.Column(db.Integer, index=True, nullable=False, default=1)
    age = db.Column(db.Integer, nullable=True)
    country = db.Column(db.String(128), nullable=True)
    city = db.Column(db.String(128), nullable=True)
    about = db.Column(db.Text, nullable=True)
    project = db.relationship('Project', cascade="all, delete-orphan")

    def to_json(self):
        return {'userId': self.id, 'email': self.email, 'name': self.name, 'type': self.type,
                'age': self.age, 'country': self.country, 'city': self.city, 'about': self.about}

    def __init__(self, id, email, name, type, age, country, city, about):
        self.id = id
        self.email = email
        self.name = name
        self.type = type
        self.age = age
        self.country = country
        self.city = city
        self.about = about


project_tag = db.Table('project_tags',
                       db.Column('project_id', db.Integer, db.ForeignKey('projects.id')),
                       db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
                       )


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    contact = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    contact_name = db.Column(db.String(128), nullable=False)
    description_long = db.Column(db.Text)
    cost = db.Column(db.String(64), index=True)
    deadlines = db.Column(db.String(64), index=True)
    website = db.Column(db.String(64), nullable=True)

    def to_json(self, tags_string):
        return {'projectId': self.id, 'name': self.name, 'contact': self.contact, 'contactName': self.contact_name,
                'descriptionLong': self.description_long, 'cost': self.cost,
                'deadlines': self.deadlines, 'website': self.website, 'tags': tags_string
                }

    def __init__(self, name, contact, contact_name, description_long, cost, deadlines, website):
        self.contact = contact
        self.name = name
        self.contact_name = contact_name
        self.description_long = description_long
        self.cost = cost
        self.deadlines = deadlines
        self.website = website


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    projects = db.relationship('Project', secondary=project_tag, backref='tags')

    def __init__(self, name):
        self.name = name

    def to_json(self):
        return {'id': self.id, 'name': self.name}


class Auth(db.Model):
    __tablename__ = 'auths'
    id = db.Column(db.Integer, primary_key=True)
    passwordToken = db.Column(db.Integer)

    def __init__(self, id, passToken):
        self.id = id
        self.passwordToken = passToken

    def to_json(self):
        return {'id': self.id, 'passwordToken': self.passwordToken}


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False, index=True)
    fromm = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    text = db.Column(db.String(1024), index=True)
    time = db.Column(db.String(64), index=True)

    def to_json(self):
        return {'id': self.id, 'chatId': self.chat_id, 'fromm': self.fromm,
                'to': self.to, 'text': self.text, 'time': self.time}

    def __init__(self, chat_id, fromm, to, text, time):
        self.chat_id = chat_id
        self.fromm = fromm
        self.to = to
        self.text = text
        self.time = time


class Chat(db.Model):
    __tablename__ = "chats"
    id = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    user2 = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    lastMessage = db.Column(db.Text, nullable=True)

    def to_json(self):
        return {'id': self.id, 'user1': self.user1, 'user2': self.user2, 'lastMessage': self.lastMessage}

    def __init__(self, user1, user2, lastMessage):
        self.user1 = user1
        self.user2 = user2
        self.lastMessage = lastMessage


class ChatShortView:
    chat_id = 0
    user_id = 0
    to_id = 0
    toName = ""
    lastMessage = ""

    def to_json(self):
        return {'chatId': self.chat_id, 'userId': self.user_id, 'toID': self.to_id, 'toName': self.toName, 'lastMessage': self.lastMessage}

    def __init__(self, chat, user_id, to_id, name, mes):
        self.chat_id = chat
        self.user_id = user_id
        self.to_id = to_id
        self.toName = name
        self.lastMessage = mes
