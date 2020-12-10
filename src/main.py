import sys
import os
import logging
from flask import Flask
from flask import jsonify
from flask import Blueprint, request, url_for, current_app
from werkzeug.utils import secure_filename
#from api.config.config import DevelopmentConfig, ProductionConfig, TestingConfig
from api.utils.database import db
from api.utils.responses import response_with
import api.utils.responses as resp
from api.routes.posts import posts_routes
from api.models.posts import Posts
from api.routes.comments import comment_routes
allowed_extensions = set(['image/jpeg', 'image/png', 'jpeg'])
def allowed_file(filename):
    return filetype in allowed_extensions
def create_app():
    UPLOAD_FOLDER = './uploads'
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =  False
    
   
    

    db.init_app(app)
    with app.app_context():
        db.create_all()
   # app.config.from_object(app_config)
    app.register_blueprint(posts_routes, url_prefix='/api/post')
    app.register_blueprint(comment_routes, url_prefix='/api/comments')
    @app.route('/image/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    @app.after_request
    def add_header(response):
        return response
    @app.errorhandler(400)
    def bad_request(e):
        logging.error(e)
        return response_with(resp.BAD_REQUEST_400)
    @app.errorhandler(500)
    def server_error(e):
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)
    @app.errorhandler(404)
    def not_found(e):
        logging.error(e)
        return response_with(resp.SERVER_ERROR_404)
   
    logging.basicConfig(stream=sys.stdout, format='%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(messages)s', level=logging.DEBUG) 
    @app.route('/')
    def index():
        return "<h1>Index route test</h1>"
    return app