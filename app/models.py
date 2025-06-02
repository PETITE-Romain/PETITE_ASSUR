from . import db
from flask_login import UserMixin
from flask_login import LoginManager
from datetime import datetime

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

class Utilisateur(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(128), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(250), nullable=False)
    prenom = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    sujet = db.Column(db.String(250), nullable=False)
    message = db.Column(db.String(250), nullable=False)