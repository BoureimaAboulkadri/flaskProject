import bcrypt
from flask import Flask, render_template, redirect, url_for, flash,request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_mysqldb import MySQL

import mysql.connector
from datetime import datetime


app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'boureima'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_PORT'] = 8889
app.config['MYSQL_DB'] = 'carPredict'
mysql = MySQL(app)

# Mysql connection


# create a data base for user
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CarPredict.db'  # Utilise une base de données SQLite nommée "site.db"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql:///carPredictPRD'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector:///root:@127.0.0.1:8889/test'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Désactive les signaux d'application pour SQLAlchemy
#app.config['MONGO_URI'] = 'mongodb://your_username:your_password@your_mongo_host:your_port/your_database'

#db = SQLAlchemy(app)

# Initialize PyMongo


# class User(db.Model):
#class User(db.Model):
  #  id = db.Column(db.Integer, primary_key=True)
   # first_name = db.Column(db.String(120), nullable=False)  # Si vous avez un champ prénom dans le formulaire d'inscription
    #last_name = db.Column(db.String(120), nullable=False)   # Si vous avez un champ nom de famille dans le formulaire d'inscription
    #email = db.Column(db.String(120), unique=True, nullable=False)
    #password = db.Column(db.String(60), nullable=False)
    #def __repr__(self) -> str:
     #   return f"User(id={self.id!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, email={self.email!r})"



#app.secret_key = 'your_secret_key_here'
class Form:

    class LoginForm(FlaskForm):
        email = StringField('Address Email', validators=[DataRequired(), Email()])
        password = PasswordField('Mot de passe', validators=[DataRequired()])
        remember_me = BooleanField('Enregistrer le mot de passe')
        submit = SubmitField('Connexion')

    class RegistrationForm(FlaskForm):
        first_name = StringField('Nom', validators=[DataRequired()])
        last_name = StringField('Prénom', validators=[DataRequired()])
        email = StringField('Address Email', validators=[DataRequired(), Email()])
        password = PasswordField('Mot de passe', validators=[DataRequired()])
      #  password_confirm = PasswordField('Confirme le mot de passe', validators=[DataRequired(), EqualTo('password', message='Les mots de passe doivent correspondre.')])
        submit = SubmitField('Inscription')

        # Custom validation methods can be added as needed, for example:
        # def validate_email(self, email):
        #     user = User.query.filter_by(email=email.data).first()
        #     if user:
        #         raise ValidationError('This email is already in use. Please choose a different one.')

    class ResetPasswordRequestForm(FlaskForm):
        email = StringField('Adresse email', validators=[DataRequired(), Email()])
        submit = SubmitField('Réinitialiser le mot de passe')





@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Form.LoginForm()
    if form.validate_on_submit():
        # 1. Récupérer l'utilisateur par e-mail
        #user = User.query.filter_by(email=form.email.data).first()

        # 2. Vérifiez si l'utilisateur existe et si le mot de passe est correct
       # if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user.password):
            # Ici, l'utilisateur est authentifié avec succès.
            # Vous pouvez, par exemple, le connecter et le rediriger vers la page d'accueil.
            # Si vous utilisez Flask-Login, vous pouvez faire login_user(user)
          #  return redirect(url_for('/'))
       # else:
            # Si l'authentification échoue, affichez un message d'erreur à l'utilisateur.
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='login', form=form)

@app.route('/test', methods=['GET', 'POST'])
def register():
    form = Form.RegistrationForm()
    if form.validate_on_submit():

        if form.validate_on_submit():
            print("Form is valid")
        else:
            print(form.errors)
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = hashed_password
        #user = User(email=form.email.data, password=hashed_password)
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)", (first_name, last_name, email, password))
            mysql.connection.commit()
            cur.close()
            flash('Your account has been created! You are now able to log in', 'success')
            #db.session.add(user)
            #db.session.commit()
        except Exception as e:
            print("Error adding user:", e)
            #db.session.rollback()

        return redirect(url_for('login'))
    return render_template('test.html', title='register', form=form)

@app.route('/password', methods=['GET', 'POST'])
def password():
    form = Form.ResetPasswordRequestForm()
    if form.validate_on_submit():
        # Logique d'envoi de l'e-mail de réinitialisation
        # Si réussi, redirigez vers une page de confirmation ou la page de connexion
        return redirect(url_for('login'))
    return render_template('password.html', title='password', form=form)



@app.route('/')
def index():
    # Lire le contenu du fichier HTML
    with open('complete_html_with_datatables.html', 'r') as file:
        table_content = file.read()
    return render_template('index.html', table=table_content)

#@app.route('/login')
#def login():
  #  return render_template('login.html', title='login')

#@app.route('/register')
#def register():
 #   return render_template('register.html', title='register')

#@app.route('/password')
#def password():
 #   return render_template('password.html', title='password')

@app.route('/layout_static')
def layout_static():
    return render_template('layout_static.html', title='layout_static')

@app.route('/layout_sidnav')
def layout_sidnav():
    return render_template('layout_sidnav.html', title='layout_sidnav')


@app.errorhandler(404)
def page_not_found(e):
    #return redirect(url_for('login'))
    return render_template('404.html'),404

@app.errorhandler(500)
def page_not_found(e):
    #return redirect(url_for('login'))
    return render_template('500.html'),500


# classs form flask_wtf import FlaskForm



if __name__ == '__main__':
    app.env = "development"
    #db.create_all()
    app.run(debug=True)
