from flask import Blueprint, abort, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Sinistre, Client
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/ajouter_sinistre', methods=['GET', 'POST'])
@login_required
@admin_required
def ajouter_sinistre():
    clients = Client.query.all()
    
    if request.method == 'POST':
        type_sinistre = request.form.get('type_sinistre')
        status = request.form.get('status')
        client_id = request.form.get('client_id')
        
        if not type_sinistre or not status or not client_id:
            flash("Tous les champs sont obligatoires.", "danger")
            return redirect(url_for('admin.ajouter_sinistre'))
        
        sinistre = Sinistre(
            type_sinistre=type_sinistre,
            status=status,
            client_id=client_id
        )
        db.session.add(sinistre)
        db.session.commit()
        
        flash("Sinistre ajouté avec succès.", "success")
        return redirect(url_for('admin.ajouter_sinistre'))

    return render_template('admin/ajouter_sinistre.html', clients=clients)
