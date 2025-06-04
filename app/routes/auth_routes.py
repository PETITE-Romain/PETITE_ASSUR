from flask import Blueprint, render_template, redirect, url_for, flash, request
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import RegisterForm
from app.models import Client
from app.forms import LoginForm
from app import db
from flask_login import login_user
from flask_login import logout_user

auth = Blueprint('auth', __name__)

@auth.route('/inscription', methods=['GET', 'POST'])
def inscription():
    form = RegisterForm()

    if form.validate_on_submit():
        prenom = form.first_name.data
        nom = form.last_name.data
        e_mail = form.email.data
        password = form.password.data
        date_naissance = form.date_naissance.data

        hashed_password = generate_password_hash(password)

        nouveau_client = Client(
            prenom=prenom,
            nom=nom,
            e_mail=e_mail,
            mot_de_passe=hashed_password,
            date_naissance=date_naissance
        )

        try:
            db.session.add(nouveau_client)
            db.session.commit()
            flash("Inscription réussie !", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur : {str(e)}", "danger")

    return render_template('inscription.html', form=form)

@auth.route('/connexion', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Recherche de l'utilisateur par email
        client = Client.query.filter_by(email=email).first()

        if client and check_password_hash(client.mot_de_passe, password):
            login_user(client)
            flash("Connexion réussie", "success")
            return redirect(url_for('main.index'))  # à adapter selon ton app
        else:
            flash("Email ou mot de passe invalide", "danger")

    return render_template('connexion.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash("Vous avez été déconnecté", "info")
    return redirect(url_for('main.index'))