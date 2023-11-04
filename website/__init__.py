from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py') # we did load settings from the config file here
    db.init_app(app)
    
    from website.views import views
    from website.auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import Meeting, Participant
    
    with app.app_context():
        db.create_all()

    return app
