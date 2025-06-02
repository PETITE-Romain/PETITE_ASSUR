from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms import RegisterForm
from app.models import Utilisateur as User
from app.forms import LoginForm
from app import db
from flask_login import login_user
from flask_login import logout_user

auth = Blueprint('auth', __name__)

@auth.route('/inscription', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Cet email est déjà utilisé.", "danger")
            return redirect(url_for('auth.register'))

        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Inscription réussie ! Vous pouvez maintenant vous connecter.", "success")
        return redirect(url_for('auth.login'))

    return render_template('inscription.html', form=form)

@auth.route('/connexion', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        if email == "admin@example.com" and password == "password":
            flash("Connexion réussie", "success")
            login_user(User)
            return redirect(url_for('main.home'))  # à adapter
        else:
            flash("Email ou mot de passe invalide", "danger")
    return render_template('connexion.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash("Vous avez été déconnecté", "info")
    return redirect(url_for('main.index'))