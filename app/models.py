# from . import db
# from flask_login import UserMixin
# from flask_login import LoginManager
# from datetime import datetime
# from sqlalchemy import Numeric, Table, Column, Integer, ForeignKey

# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'

# class Souscrit(db.Model):
#     __tablename__ = 'souscrit'
#     client_id = db.Column(db.Integer, db.ForeignKey('client.id'), primary_key=True)
#     contrat_id = db.Column(db.Integer, db.ForeignKey('contrat_assurance.id'), primary_key=True)
#     # d'autres colonnes si besoin

#     client = db.relationship('Utilisateur', back_populates='souscriptions')
#     contrat = db.relationship('contrat_assurance', back_populates='souscriptions')

# class Utilisateur(db.Model, UserMixin):
#     __tablename__ = 'client'
#     id = db.Column(db.Integer, primary_key=True)
#     nom = db.Column(db.String(100))
#     prenom = db.Column(db.String(100))
#     e_mail = db.Column(db.String(100))
#     mot_de_passe = db.Column(db.String(255))
#     date_naissance = db.Column(db.Date)

#     contrats = db.relationship(
#         'contrat_assurance',
#         secondary='souscrit',
#         primaryjoin='Utilisateur.id == Souscrit.client_id',
#         secondaryjoin='contrat_assurance.id == Souscrit.contrat_id',
#         back_populates='clients',
#         viewonly=True
#     )
#     souscriptions = db.relationship('Souscrit', back_populates='client')


# class contrat_assurance(db.Model):
#     __tablename__ = 'contrat_assurance'
#     id = db.Column(db.Integer, primary_key=True)
#     tarif_final = db.Column(db.Numeric(10, 2))
#     date_souscription = db.Column(db.Date)

#     type_contrat_assurance_id = db.Column(db.Integer, db.ForeignKey('type_contrat_assurance.id'))

#     souscriptions = db.relationship('Souscrit', back_populates='contrat')
#     type_contrat = db.relationship('TypeContratAssurance', backref='contrats')
#     clients = db.relationship(
#         'Utilisateur',
#         secondary='souscrit',
#         primaryjoin='contrat_assurance.id == Souscrit.contrat_id',
#         secondaryjoin='Utilisateur.id == Souscrit.client_id',
#         back_populates='contrats',
#         viewonly=True
#     )


# class TypeContratAssurance(db.Model):
#     __tablename__ = 'type_contrat_assurance'
#     id = db.Column(db.Integer, primary_key=True)
#     libelle = db.Column(db.String(250))
#     description = db.Column(db.String(250))

# @login_manager.user_loader
# def load_user(user_id): 
#     return Utilisateur.query.get(int(user_id))

# class Contact(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nom = db.Column(db.String(250), nullable=False)
#     prenom = db.Column(db.String(250), nullable=False)
#     email = db.Column(db.String(250), nullable=False)
#     sujet = db.Column(db.String(250), nullable=False)
#     message = db.Column(db.String(250), nullable=False)

# class Sinistre(db.Model):
#     __tablename__ = 'sinistre'
#     id = db.Column(db.Integer, primary_key=True)
#     type_sinistre = db.Column(db.String(100), nullable=False)
#     status = db.Column(db.String(50), nullable=False)

#     # Relation avec les justificatifs via la table 'justifier'
#     justificatifs = db.relationship(
#         'Justificatif',
#         secondary='justifier',
#         backref='sinistres',
#         lazy='dynamic'
#     )

#     def __repr__(self):
#         return f'<Sinistre {self.id} - {self.type_sinistre} - {self.status}>'

# class Justificatif(db.Model):
#     __tablename__ = 'justificatif'
#     id = db.Column(db.Integer, primary_key=True)
#     description_sinistre = db.Column(db.Text, nullable=True)
#     type_justificatif = db.Column(db.String(100), nullable=False)

#     def __repr__(self):
#         return f'<Justificatif {self.id} - {self.type_justificatif}>'

# class Justifier(db.Model):
#     __tablename__ = 'justifier'
#     sinistre_id = db.Column(db.Integer, db.ForeignKey('sinistre.id'), primary_key=True)
#     justificatif_id = db.Column(db.Integer, db.ForeignKey('justificatif.id'), primary_key=True)

from flask_login import UserMixin
from app import db
from sqlalchemy import (
    Column, Integer, String, Date, DateTime, ForeignKey, Table, Text, DECIMAL, create_engine, Boolean
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# ============================
# Tables d'association (liaison)
# ============================

ajouter = Table(
    'ajouter', db.Model.metadata,
    Column('client_id', Integer, ForeignKey('client.id'), primary_key=True),
    Column('piece_id', Integer, ForeignKey('pieces_obligatoires.id'), primary_key=True)
)

associer = Table(
    'associer', db.Model.metadata,
    Column('client_id', Integer, ForeignKey('client.id'), primary_key=True),
    Column('voyageur_id', Integer, ForeignKey('voyageur.id'), primary_key=True)
)

souscrit = Table(
    'souscrit', db.Model.metadata,
    Column('client_id', Integer, ForeignKey('client.id'), primary_key=True),
    Column('contrat_id', Integer, ForeignKey('contrat_assurance.id'), primary_key=True)
)

est_lie_a = Table(
    'est_lie_a', db.Model.metadata,
    Column('contrat_id', Integer, ForeignKey('contrat_assurance.id'), primary_key=True),
    Column('voyage_id', Integer, ForeignKey('voyage.id'), primary_key=True)
)

correspondre = Table(
    'correspondre', db.Model.metadata,
    Column('voyage_id', Integer, ForeignKey('voyage.id'), primary_key=True),
    Column('pays_id', Integer, ForeignKey('pays.id'), primary_key=True)
)

utiliser = Table(
    'utiliser', db.Model.metadata,
    Column('voyage_id', Integer, ForeignKey('voyage.id'), primary_key=True),
    Column('vol_id', Integer, ForeignKey('vols.id'), primary_key=True)
)

contenir = Table(
    'contenir', db.Model.metadata,
    Column('contrat_id', Integer, ForeignKey('contrat_assurance.id'), primary_key=True),
    Column('assurance_id', Integer, ForeignKey('assurances.id'), primary_key=True)
)

declarer = Table(
    'déclarer', db.Model.metadata,
    Column('sinistre_id', Integer, ForeignKey('sinistre.id'), primary_key=True),
    Column('contrat_id', Integer, ForeignKey('contrat_assurance.id'), primary_key=True)
)

operer = Table(
    'opérer', db.Model.metadata,
    Column('vol_id', Integer, ForeignKey('vols.id'), primary_key=True),
    Column('compagnie_id', Integer, ForeignKey('compagnie.id'), primary_key=True)
)

appartenir = Table(
    'appartenir', db.Model.metadata,
    Column('compagnie_id', Integer, ForeignKey('compagnie.id'), primary_key=True),
    Column('contact_id', Integer, ForeignKey('contact_compagnie.id'), primary_key=True)
)

avoir = Table(
    'avoir', db.Model.metadata,
    Column('sinistre_id', Integer, ForeignKey('sinistre.id'), primary_key=True),
    Column('piece_id', Integer, ForeignKey('pieces_obligatoires.id'), primary_key=True)
)

justifier = Table(
    'justifier', db.Model.metadata,
    Column('sinistre_id', Integer, ForeignKey('sinistre.id'), primary_key=True),
    Column('justificatif_id', Integer, ForeignKey('justificatif.id'), primary_key=True)
)

deposer = Table(
    'déposer', db.Model.metadata,
    Column('justificatif_id', Integer, ForeignKey('justificatif.id'), primary_key=True),
    Column('client_id', Integer, ForeignKey('client.id'), primary_key=True)
)

# ============================
# Tables principales
# ============================

class Client(db.Model, UserMixin):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True)
    nom = Column(String(100))
    prenom = Column(String(100))
    e_mail = Column(String(100))
    mot_de_passe = Column(String(255), nullable=False)
    date_naissance = Column(Date)
    is_admin = db.Column(Boolean, default=False, nullable=False)

    pieces = relationship("PiecesObligatoires", secondary=ajouter)
    voyageurs = relationship("Voyageur", secondary=associer)
    contrats = relationship("ContratAssurance", secondary=souscrit)
    justificatifs = relationship("Justificatif", secondary=deposer)
    sinistres = db.relationship('Sinistre', back_populates='client', cascade="all, delete-orphan")
    contrats = db.relationship('ContratAssurance', back_populates='client', cascade='all, delete-orphan')


class Voyageur(db.Model):
    __tablename__ = 'voyageur'

    id = Column(Integer, primary_key=True)
    nom = Column(String(100))
    prenom = Column(String(100))
    date_naissance = Column(Date)
    lien_parente = Column(String(100))


class Voyage(db.Model):
    __tablename__ = 'voyage'

    id = Column(Integer, primary_key=True)
    duree_minutes = Column(Integer)
    date_depart = Column(Date)
    date_retour = Column(Date)
    tarif = Column(DECIMAL(10, 2))

    pays = relationship("Pays", secondary=correspondre)
    vols = relationship("Vols", secondary=utiliser)


class Pays(db.Model):
    __tablename__ = 'pays'

    id = Column(Integer, primary_key=True)
    pays_destination = Column(String(100))
    coef_pays_dest = Column(DECIMAL(5, 2))


class Vols(db.Model):
    __tablename__ = 'vols'

    id = Column(Integer, primary_key=True)
    numero_vol = Column(String(50))

    compagnies = relationship("Compagnie", secondary=operer)


class Compagnie(db.Model):
    __tablename__ = 'compagnie'

    id = Column(Integer, primary_key=True)
    nom = Column(String(100))
    malus_bonus = Column(DECIMAL(5, 2))

    contacts = relationship("ContactCompagnie", secondary=appartenir)


class ContactCompagnie(db.Model):
    __tablename__ = 'contact_compagnie'

    id = Column(Integer, primary_key=True)
    nom = Column(String(100))
    prenom = Column(String(100))
    email = Column(String(100))
    telephone = Column(String(20))


class Sinistre(db.Model):
    __tablename__ = 'sinistre'

    id = Column(Integer, primary_key=True)
    type_sinistre = Column(String(100))
    status = Column(String(50))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

    client = db.relationship('Client', back_populates='sinistres')
    contrats = relationship("ContratAssurance", secondary=declarer)
    pieces = relationship("PiecesObligatoires", secondary=avoir)
    justificatifs = relationship("Justificatif", secondary=justifier)


class Justificatif(db.Model):
    __tablename__ = 'justificatif'

    id = Column(Integer, primary_key=True)
    description_sinistre = Column(Text)
    type_justificatif = Column(String(100))


class PiecesObligatoires(db.Model):
    __tablename__ = 'pieces_obligatoires'

    id = Column(Integer, primary_key=True)
    type_piece = Column(String(100))


class Assurances(db.Model):
    __tablename__ = 'assurances'

    id = Column(Integer, primary_key=True)
    type_assurance = Column(String(100))
    tarif = Column(DECIMAL(10, 2))


class TypeContratAssurance(db.Model):
    __tablename__ = 'type_contrat_assurance'

    id = Column(Integer, primary_key=True)
    libelle = Column(String(250))
    description = Column(String(250))


class ContratAssurance(db.Model):
    __tablename__ = 'contrat_assurance'

    id = Column(Integer, primary_key=True)
    tarif_final = Column(DECIMAL(10, 2))
    date_souscription = Column(Date)
    type_contrat_assurance_id = Column(Integer, ForeignKey('type_contrat_assurance.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

    type_contrat = relationship("TypeContratAssurance")
    voyages = relationship("Voyage", secondary=est_lie_a)
    assurances = relationship("Assurances", secondary=contenir)
    client = db.relationship('Client', back_populates='contrats')


class Contact(db.Model):
    __tablename__ = 'contact'

    id = Column(Integer, primary_key=True)
    nom = Column(String(250))
    prenom = Column(String(250))
    email = Column(String(250))
    sujet = Column(String(250))
    message = Column(String(250))
    date_envoie = Column(DateTime)
