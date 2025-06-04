from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler
import os
from sqlalchemy.pool import NullPool

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,         # Vérifie si la connexion est toujours active
    "pool_recycle": 280,           # Recycle la connexion toutes les 280 secondes (~4 min 40)
    "poolclass": NullPool          # (Optionnel) désactive le pooling pour tests simples
    }

    if not os.path.exists('logs'):
        os.mkdir('logs')

    file_handler = RotatingFileHandler('logs/site.log', maxBytes=10240, backupCount=3)
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s in %(pathname)s:%(lineno)d'
    )
    file_handler.setFormatter(formatter)
    
    login_manager = LoginManager()
    login_manager.init_app(app)

    from app.models import Client

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Client, int(user_id))


    app.config.from_object('config')

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Application démarrée')

    db.init_app(app)

    from .routes.user_routes import user
    app.register_blueprint(user, url_prefix='/user')
    from .routes.souscription_routes import souscription_bp
    app.register_blueprint(souscription_bp, url_prefix='/souscription')
    from .routes.main_routes import main
    app.register_blueprint(main)
    from .routes.auth_routes import auth
    app.register_blueprint(auth)
    from app.routes.admin_routes import admin_bp
    app.register_blueprint(admin_bp)


    return app

