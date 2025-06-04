from flask import Blueprint, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename

sinistre_bp = Blueprint('sinistre', __name__)

@sinistre_bp.route('/ajouter_justificatif', methods=['POST'])
@login_required
def ajouter_justificatif():
    sinistre_id = request.form.get('sinistre_id')
    commentaire = request.form.get('commentaire')
    fichier = request.files.get('justificatif')

    if not fichier:
        flash("Aucun fichier reçu.")
        return redirect(url_for('sinistre.mes_sinistres'))

    nom_fichier = secure_filename(fichier.filename)
    dossier_upload = os.path.join(current_app.config['UPLOAD_FOLDER'], 'justificatifs')
    os.makedirs(dossier_upload, exist_ok=True)
    chemin_fichier = os.path.join(dossier_upload, nom_fichier)
    fichier.save(chemin_fichier)

    # TODO : Ajouter en base de données un lien entre sinistre_id, user, commentaire, fichier...

    flash("Justificatif envoyé avec succès.")
    return redirect(url_for('sinistre.mes_sinistres'))
