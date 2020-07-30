# -*- encoding utf-8 -*-

from flask import current_app as app
from flask import request, abort, json
from flask_login import login_user, logout_user

from app import login_manager, db
from app.models import Auth, User, Project


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/login')
def login():
    id = int(request.args.get('id'))
    pass_hash = int(request.args.get('passwordToken'))
    auth = Auth.query.filter_by(id=id).first()
    user = None
    if pass_hash == auth.passwordToken:
        user = User.query.get(id)
    if user:
        login_user(user)
        return json.jsonify(user.to_json())
    else:
        abort(401)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/logout')
def logout():
    logout_user()
    return 200


@app.route('/registr')
def registr():
    id = int(request.args.get('id'))
    email = request.args.get('email')
    name = request.args.get('name')
    passwordToken = int(request.args.get('passwordToken'))
    type = int(request.args.get('type'))
    auth = Auth(id, passwordToken)
    user = User(id, name, email, type, None, None, None)
    db.session.add(auth)
    db.session.add(user)
    db.session.commit()
    return json.jsonify(user.to_json())


@app.route('/projects/<project_id>')
def get_project_by_id(project_id):
    project = [i for i in Project.query.all() if i['id'] == int(project_id)]
    if len(project) == 0:
        abort(404)
    return json.jsonify(project[0])


@app.route('/projects', methods=['GET'])
def get_projects():
    projects = [i.to_json() for i in Project.query.all()]
    return json.jsonify(projects)


@app.route('/projects/my/<id>')
def get_projects_by_contact(id):
    projects = [i.to_json() for i in Project.query.filter_by(contact=id).all()]
    return json.jsonify(projects)


@app.route('/users', methods=['GET'])
def get_users():
    users = [i.to_json() for i in User.query.all()]
    return json.jsonify(users)


@app.route('/users/<id>')
def get_user_by_id(id):
    return json.jsonify(User.query.get(id).to_json())


# @app.route('/create_all')
# def create_all():
#       user = User(1761161690, 'cita_del@citadel.ru', 'CITADEL', 1, None, None,  None)
#       db.session.add(user)
#       user = User(-1235243292, 'unknown@un.known', 'Company you need', 0, None, None, None)
#       db.session.add(user)
#     auth = Auth(1761161690, -1861353340)
#     db.session.add(auth)
#     auth = Auth(-1235243292, -1861353340)
#     db.session.add(auth)
#         project = Project('RISE', 1761161690, 'The best startup platform ever',
#                           'Some very long text which i definitely don\'t won\'t to type so it\'s kinda short text',
#                           '1000000 рублей', '1 месяц', 'http://bestApp.ever/RISE')
#         db.session.add(project)
#         project = Project('CITADEL Education', 1761161690, 'The best education platform ever',
#                           'Some very long text which i definitely don\'t won\'t to type so it\'s kinda short text',
#                           '1100000 рублей', '2 месяца', 'http://bestApp.ever/Education')
#         db.session.add(project)
#     db.session.commit()
#     return str(200)


@app.route('/delete')
def delete():
    Auth.query.filter_by(id=1761161690).delete()
    Auth.query.filter_by(id=-1235243292).delete()
    User.query.filter_by(id=1761161690).delete()
    User.query.filter_by(id=-1235243292).delete()
    db.session.commit()
    return "200"
