import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'flaskapp.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JPG_UPLOAD_DIR = os.path.join(basedir, 'static/profile_pics')

    PERMANENT_SESSION_LIFETIME = timedelta(days=7)  # 设置session的保存时间