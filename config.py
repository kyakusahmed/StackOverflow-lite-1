import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'te7654vtt$$@%^78(sx$3t998ing'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'wuiq2739%W%$%^FhjY^^'
    DEBUG = True
    TESTING = True
    # DATABASE_URI
