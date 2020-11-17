import os
from flask import Flask
from flask import jsonify
from api.config.config import DevelopmentConfig, ProductionConfig, TestingConfig
from api.utils.database import db

def create_app(config):
    app = Flask(__name__)
    if os.environ.get('WORK_ENV') == 'PROD':
        app_config = ProductionConfig
    elif os.environ.get('WORK_ENV') == 'TEST':
        app_config = TestingConfig
    else:
        app_config = DevelopmentConfig
    app.config.from_object(app_config)
   
    db.init_app()
    with app.app_context():
        db.create_all()
    return app