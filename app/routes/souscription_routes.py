from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from datetime import datetime

from app import db
from app.models import ContratAssurance, TypeContratAssurance, souscrit

souscription_bp = Blueprint('souscription', __name__)

# Exemple de fonction tarifaire simple
def calcul_prix(date_naissance, pays, duree_jours):
    age = (datetime.today().date() - date_naissance).days // 365
    base = 10.0 
    if age < 18:
        base *= 0.8
    elif age > 60:
        base *= 1.5
    if pays.lower() in ['usa', 'canada', 'australie']:
        base *= 2
    base *= duree_jours / 7
    return round(base, 2)

@souscription_bp.route('/souscrire', methods=['GET', 'POST'])
@login_required
def souscrire():
    types_contrats = TypeContratAssurance.query.all()
    devis = None

    if request.method == 'POST':
        action = request.form.get('action')
        type_id = request.form.get('type_contrat_id')
        pays = request.form.get('pays')

        # Récupération sécurisée de la durée
        try:
            duree = int(request.form.get('duree'))
        except (TypeError, ValueError):
            flash("Durée invalide.", "danger")
            return redirect(url_for('souscription.souscrire'))

        # Gestion de la date de naissance
        if current_user.date_naissance:
            date_naissance = current_user.date_naissance
        else:
            date_naissance_str = request.form.get('date_naissance')
            if not date_naissance_str:
                flash("La date de naissance est requise.", "danger")
                return redirect(url_for('souscription.souscrire'))
            try:
                date_naissance = datetime.strptime(date_naissance_str, "%Y-%m-%d").date()
            except ValueError:
                flash("Format de date invalide. Utilisez AAAA-MM-JJ.", "danger")
                return redirect(url_for('souscription.souscrire'))

        prix = calcul_prix(date_naissance, pays, duree)

        # Si bouton "Obtenir un devis"
        if action == 'devis':
            devis = {
                "type_id": type_id,
                "tarif": prix,
                "pays": pays,
                "duree": duree
            }
            return render_template(
                'souscription.html',
                devis=devis,
                types_contrats=types_contrats,
                user=current_user
            )

        # Si bouton "Souscrire"
        elif action == 'souscrire':
            if not type_id:
                flash("Veuillez sélectionner un type de contrat.", "danger")
                return redirect(url_for('souscription.souscrire'))

            contrat = ContratAssurance(
                tarif_final=prix,
                date_souscription=datetime.utcnow(),
                type_contrat_assurance_id=type_id,
                client_id=current_user.id
            )
            db.session.add(contrat)
            db.session.commit()

            flash("Souscription enregistrée avec succès !", "success")
            return redirect(url_for('user.profil'))

        else:
            flash("Action non reconnue.", "danger")
            return redirect(url_for('souscription.souscrire'))

    return render_template(
        'souscription.html',
        types_contrats=types_contrats,
        devis=devis,
        user=current_user
    )
