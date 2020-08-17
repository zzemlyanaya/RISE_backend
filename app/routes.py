# -*- encoding utf-8 -*-

from flask import current_app as app
from flask import request, json
from flask_login import login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError

from app import login_manager, db
from app.models import Auth, User, Project, Tag, Chat, Message, ChatShortView


# INIT ROUTE

@app.route('/')
def index():
    return json.jsonify({'error': None, 'data': 'OK'})


# LOGIN ROUTES

@app.route('/login')
def login():
    user_id = int(request.args.get('id'))
    pass_hash = int(request.args.get('passwordToken'))
    keep_auth = request.args.get('keepAuth')
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return json.jsonify({'error': 'Неверный логин/пароль',
                             'data': None})
    auth = Auth.query.filter_by(id=user_id).first()
    user = None
    if auth is not None and pass_hash == auth.passwordToken:
        user = User.query.get(user_id)
    if user:
        login_user(user, remember=keep_auth)
        return json.jsonify({'error': None, 'data': user.to_json()})
    else:
        return json.jsonify({'error': 'Неверный логин/пароль',
                             'data': None})


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/logout')
def logout():
    logout_user()
    return json.jsonify({'error': None, 'data': 'OK'})


@app.route('/registr')
def registr():
    user_id = int(request.args.get('id'))
    email = request.args.get('email')
    existing_user = User.query.filter_by(email=email).first()
    if existing_user is not None:
        return json.jsonify({'error': 'Пользователь с таким email уже существует',
                             'data': None})
    name = request.args.get('name')
    password_token = int(request.args.get('passwordToken'))
    typee = int(request.args.get('type'))
    auth = Auth(user_id, password_token)
    user = User(user_id, email, name, typee, None, None, None, None)
    db.session.add(auth)
    db.session.add(user)
    db.session.commit()
    login_user(user, remember=False)
    return json.jsonify({'error': None, 'data': user.to_json()})


# PROJECTS ROUTES

@login_required
@app.route('/projects', methods=['GET'])
def get_projects():
    projects = [i.to_json(tags_to_string(i.tags)) for i in Project.query.all()]
    return json.jsonify({'error': None, 'data': projects})


def tags_to_string(tags):
    return ','.join([i.name for i in tags])


@login_required
@app.route('/projects', methods=['POST'])
def add_project():
    data = request.json['nameValuePairs']
    project = None
    try:
        project = Project.query.filter_by(name=data['name']).first()
        if project is not None:
            project.name = data['name']
            project.deadlines = data['deadlines']
            project.description_long = data['descriptionLong']
            project.cost = data['cost']
            project.website = data['website']
        else:
            project = Project(data['name'], data['contact'], data['contactName'], data['descriptionLong'],
                              data['cost'], data['deadlines'], data['website'])

        if data['tags'] != '':
            tags = [Tag(i) for i in data['tags'].split(',')]
            for i in tags:
                if Tag.query.filter_by(name=i.name).first() is None:
                    db.session.add(i)
            project.tags.clear()
            project.tags.extend(tags)
        db.session.add(project)
        db.session.commit()
        return json.jsonify({'error': None, 'data': 'OK'})
    except IntegrityError as e:
        print(getattr(e, 'message', repr(e)))
        return json.jsonify({'error': 'Проект с таким названием уже существует.', 'data': None})
    except Exception as e:
        db.session.rollback()
        print(getattr(e, 'message', repr(e)))
        return json.jsonify({'error': 'Что-то пошло не так! Попробуйте ещё раз.', 'data': None})


@login_required
@app.route('/projects/<project_id>', methods=['GET'])
def get_project_by_id(project_id):
    project = [i for i in Project.query.all() if i['id'] == int(project_id)]
    if len(project) == 0:
        return json.jsonify({'error': 'Проект не найден',
                             'data': None})
    return json.jsonify({'error': None, 'data': project[0]})


@login_required
@app.route('/projects/<project_id>', methods=['DELETE'])
def delete_project_by_id(project_id):
    try:
        Project.query.filter_by(id=project_id).delete()
        db.session.commit()
        return json.jsonify({'error': None, 'data': 'OK'})
    except Exception as e:
        db.session.rollback()
        print(getattr(e, 'message', repr(e)))
        return json.jsonify({'error': 'Что-то пошло не так! Попробуйте ещё раз.', 'data': None})


@login_required
@app.route('/projects/my/<proj_id>', methods=['GET'])
def get_projects_by_contact(proj_id):
    if request.method == 'GET':
        projects = [i.to_json(tags_to_string(i.tags)) for i in Project.query.filter_by(contact=proj_id).all()]
        return json.jsonify({'error': None, 'data': projects})
    else:
        return str(200)


@login_required
@app.route('/projects/by_tag/<tag>')
def get_projects_by_tag(tag):
    tag_from_db = Tag.query.filter_by(name=tag).first()
    projects = [i.to_json() for i in tag_from_db.projects]
    return json.jsonify({'error': None, 'data': projects})


# USERS ROUTES

@login_required
@app.route('/users', methods=['GET'])
def get_users():
    users = [i.to_json() for i in User.query.all()]
    return json.jsonify({'error': None, 'data': users})


@login_required
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json['nameValuePairs']
    user = None
    try:
        user = User.query.filter_by(id=data['userId']).first()
        if user is not None:
            user.name = data['name']
            # TODO update user
        else:
            user = User(data['userId'], data['email'], data['name'], data['type'], data['age'], data['country'],
                        data['city'], data['about'])
        db.session.add(user)
        db.session.commit()
        return json.jsonify({'error': None, 'data': 'OK'})
    except Exception as e:
        db.session.rollback()
        print(getattr(e, 'message', repr(e)))
        return json.jsonify({'error': 'Что-то пошло не так! Попробуйте ещё раз.', 'data': None})


@login_required
@app.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    return json.jsonify({'error': None, 'data': User.query.get(user_id).to_json()})


@login_required
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    User.query.filter_by(id=user_id).delete()
    return json.jsonify({'error': None, 'data': 'OK'})


# TAGS ROUTES

@app.route('/tags')
def get_tags():
    tags = [i.to_json() for i in Tag.query.all()]
    return json.jsonify({'error': None, 'data': tags})


# CHATS ROUTES

@app.route('/chats', methods=['GET'])
def get_all_chats():
    chats = [i.to_json() for i in Chat.query.all()]
    return json.jsonify({'error': None, 'data': chats})


@login_required
@app.route('/chats', methods=['POST'])
def add_chat():
    data = request.json['nameValuePairs']
    chat = Chat(data['user1'], data['user2'], data['lastMessage'])
    try:
        db.session.add(chat)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(getattr(e, 'message', repr(e)))
        return json.jsonify({'error': 'Что-то пошло не так! Попробуйте ещё раз.', 'data': None})


@login_required
@app.route('/chats/<chat_id>', methods=['GET'])
def get_chat_by_id(chat_id):
    messages = [i.to_json() for i in Message.query.filter_by(chat_id=chat_id).order_by(Message.time).all()]
    return json.jsonify({'error': None, 'data': messages})


@login_required
@app.route('/chats/<chat_id>', methods=['DELETE'])
def delete_chat_by_id(chat_id):
    Chat.query.filter_by(id=chat_id).delete()
    return json.jsonify({'error': None, 'data': 'OK'})


@login_required
@app.route('/chats/by_user/<user_id>')
def get_chats_by_user(user_id):
    chats = Chat.query.filter_by(user1=user_id).all()
    chats.extend(Chat.query.filter_by(user2=user_id).all())
    res = []
    for i in chats:
        if i.user1 == int(user_id):
            to = int(i.user2)
        else:
            to = int(i.user1)
        res.append(ChatShortView(i.id, user_id, to, User.query.get(to).name, i.lastMessage).to_json())
    return json.jsonify({'error': None, 'data': res})


# OTHER ROUTES

@app.errorhandler(500)
def not_found(error):
    db.session.rollback()
    return json.jsonify({'error': error.specific,
                         'data': None})


@app.route('/create_all')
def create_all():
    db.create_all()
    user = User(1761161690, 'cita_del@citadel.ru', 'CITADEL', 1, None, None, None, None)
    db.session.add(user)
    user = User(-1235243292, 'unknown@un.known', 'Company you need', 0, None, None, None, None)
    db.session.add(user)
    auth = Auth(1761161690, -1861353340)
    db.session.add(auth)
    auth = Auth(-1235243292, -1861353340)
    db.session.add(auth)

    tagAndroid = Tag('Android')
    tagWeb = Tag('Web')
    tagAI = Tag('AI')
    tagB = Tag('B2B')
    tagC = Tag('B2C')
    tagG = Tag('B2G')
    tagEd = Tag('Education')
    db.session.add_all([tagAndroid, tagAI, tagB, tagEd, tagWeb, tagC, tagG])
    db.session.commit()

    project = Project(name='RISE', contact=1761161690, contact_name='CITADEL',
                      description_long='The best startup platform ever',
                      cost='100 000', deadlines='1 месяц', website='http://bestApp.ever/RISE')
    project.tags.extend([tagAndroid, tagB, tagC, tagG])
    db.session.add(project)
    project1 = Project('CITADEL Education', 1761161690, 'CITADEL', 'The best education platform ever',
                       '110 000 000', '2 месяца', 'http://bestApp.ever/Education')
    project1.tags.extend([tagAI, tagEd, tagWeb])
    db.session.add(project1)

    chat = Chat(1761161690, -1235243292, "Hi there!")
    db.session.add(chat)

    message = Message(1, 1761161690, -1235243292, "Hi there!", "0.0.00 00:00")
    db.session.add(message)

    db.session.commit()
    return str(200)
