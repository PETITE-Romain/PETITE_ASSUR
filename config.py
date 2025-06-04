import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://u347282350_petiteassur:PetiteAssur123!@92.113.22.49:3306/u347282350_petiteassur'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'cle-secrete-de-dev')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
