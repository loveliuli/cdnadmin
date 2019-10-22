class Config(object):
    SECRET_KEY = '******'
    RECAPTCHA_PUBLIC_KEY = '******'
    RECAPTCHA_PRIVATE_KEY = '******'


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'


class DevConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = '******'

