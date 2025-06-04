from flask import Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename
import os
from flask_login import login_required, current_user
from app.models import ContratAssurance, Sinistre

user = Blueprint('user', __name__)


@user.route('/sinistres')
@login_required
def sinistres():
    sinistres = Sinistre.query.filter_by(client_id=current_user.id).all()
    return render_template('sinistres.html', sinistres=sinistres)

@user.route('/profil')
@login_required
def profil():
    contrats = current_user.contrats
    return render_template('profil.html', utilisateur=current_user, contrats=contrats)

@user.route('/ajouter-justificatif', methods=['POST'])
@login_required
def ajouter_justificatif():
    sinistre_id = request.form.get('sinistre_id')
    fichier = request.files.get('justificatif')
    commentaire = request.form.get('commentaire')

    if fichier:
        filename = secure_filename(fichier.filename)
        chemin = os.path.join("uploads", "justificatifs", fichier.filename)
        os.makedirs(os.path.dirname(chemin), exist_ok=True)
        chemin = os.path.join('uploads/justificatifs', filename)
        fichier.save(chemin)

        # Ajoute une ligne à la table justificatifs, si tu as un modèle
        # Sinon ajoute les infos à ton modèle Sinistre par exemple

        flash("Justificatif ajouté avec succès", "success")
    else:
        flash("Aucun fichier fourni", "danger")
    return redirect(url_for('user.profil'))