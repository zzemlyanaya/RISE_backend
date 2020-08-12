from flask import json
from app import socketio, db
from flask_socketio import join_room, leave_room, send, emit

from app.models import Message, Chat


@socketio.on('message', namespace='/chat')
def test_message(message_json):
    message = Message(message_json['chatId'], message_json['fromm'], message_json['to'], message_json['text'],
                      message_json['time'])
    db.session.add(message)
    chat = Chat.query.filter_by(id=int(message_json['chatId'])).first()
    chat.lastMessage = message_json['text']
    db.session.commit()
    send(message.to_json(), namespace='/chat', room=message_json['chatId'])
    print('RECEIVED:', message_json['text'])


@socketio.on('join', namespace='/chat')
def on_join(data):
    chat_id = data['chatId']
    print('JOINED')
    join_room(chat_id)


@socketio.on('leave', namespace='/chat')
def on_leave(data):
    chat_id = data['chatId']
    print('LEFT')
    leave_room(chat_id)
