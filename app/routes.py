# -*- encoding utf-8 -*-
from flask import request, make_response, abort, json
from flask_login import current_user, login_user, logout_user

from app import app, login_manager
from app.models import Auth, User, Project


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return json.jsonify(current_user.to_json())
    id = request.args.get('id')
    pass_hash = request.args.get('passwordHash')
    auth = Auth.query.filter_by(id=id).first()
    user = None
    if pass_hash == auth.passwordToken:
        user = User.query.get()
    if user:
        login_user(user, remember=True)
        return json.jsonify(user.to_json())
    else:
        return 401


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/logout')
def logout():
    logout_user()
    return 200


@app.errorhandler(404)
def not_found(error):
    return make_response(json.jsonify({'error': 'Not found'}), 404)


@app.errorhandler(500)
def not_found(error):
    return make_response(json.jsonify({'error': 'Server error'}), 500)


@app.route('/projects/<project_id>')
def get_project_by_id(project_id):
    project = [i for i in projects if i['id'] == int(project_id)]
    if len(project) == 0:
        abort(404)
    return json.jsonify(project[0])


projects = [
    {
        'id': 1,
        'name': 'RISE',
        'contact': 1761161690,
        'descriptionShort': 'The best startup platform ever',
        'descriptionLong': 'Some very long text which i definitely don\'t won\'t to type so it\'s kinda short text',
        'cost': '1000000 рублей',
        'deadlines': '1 месяц',
        'website': 'http://bestApp.ever/RISE'
    },
    {
        'id': 2,
        'name': 'CITADEL Education',
        'contact': 1761161690,
        'descriptionShort': 'The best education platform ever',
        'descriptionLong': 'Some very long text which i definitely don\'t won\'t to type so it\'s kinda short text',
        'cost': u'1100000 рублей',
        'deadlines': u'2 месяца',
        'website': 'http://bestApp.ever/C_Education'
    }
]


@app.route('/projects', methods=['GET'])
def get_tasks():
    return json.jsonify(projects)
