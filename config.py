import os
app_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you*will*never*know'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(app_dir, 'rise.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG=True
    JSON_AS_ASCII=False

    HOST='0.0.0.0'
    PORT='5000'

    UPLOAD_FOLDER = os.path.join(app_dir, 'files')
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'svg', 'mp4', 'mov'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
