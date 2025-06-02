from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    from .models import login_manager
    login_manager.init_app(app)

    from .routes.main_routes import main
    app.register_blueprint(main)
    from .routes.auth_routes import auth
    app.register_blueprint(auth)


    return app
