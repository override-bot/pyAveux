import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config (object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI =  'sqlite:///'+os.path.join(basedir, 'db.sqlite')

class DevelopmentConfig(Config):
     DEBUG = True
   SQLALCHEMY_DATABASE_URI =  'sqlite:///'+os.path.join(basedir, 'db.sqlite')
     SQLALCHEMY_ECHO = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')
    SQLALCHEMY_ECHO = False