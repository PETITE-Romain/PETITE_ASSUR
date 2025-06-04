from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegisterForm(FlaskForm):
    first_name = StringField('Prénom', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Nom', validators=[DataRequired(), Length(max=50)])
    email = StringField('Adresse email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(), EqualTo('password', message="Les mots de passe doivent être identiques.")
    ])
    date_naissance = DateField('Date de naissance', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField("S'inscrire")

class LoginForm(FlaskForm):
    email = StringField("Adresse email", validators=[DataRequired(), Email()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Se connecter")