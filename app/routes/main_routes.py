from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from ..models import Client
from app.models import Contact
from sqlalchemy import insert

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/utilisateurs')
def liste_utilisateurs():
    utilisateurs = Client.query.all()
    return render_template('utilisateurs.html', utilisateurs=utilisateurs)

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        e_mail = request.form['email']
        sujet = request.form['sujet']
        message = request.form['message']

        print(nom, prenom, e_mail, sujet, message)

        from app import db

        nouveau_contact = Contact(
            nom=nom,
            prenom=prenom,
            e_mail=e_mail,
            sujet=sujet,
            message=message
        )

        try:
            db.session.add(nouveau_contact)
            db.session.commit()
            flash("Votre message a été envoyé avec succès !", "success")
            current_app.logger.info(f"Nouveau message de contact : {e_mail}, sujet : {sujet}")
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur : {str(e)}", "danger")
            current_app.logger.error(f"Erreur contact : {str(e)}")
            flash("Une erreur est survenue. Veuillez réessayer.", "danger")
        
        return redirect(url_for('main.contact'))
    
    return render_template('contact.html')