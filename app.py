from flask import Flask, render_template, request, url_for, redirect, flash
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Password@localhost/accounts'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class RegistrationForm(Form):
    fullname = StringField('fullname', [validators.Length(min = 1, max = 50)])
    email = StringField('email', [validators.DataRequired(), validators.Length(min = 1, max = 50)])
    username = StringField('username', [validators.DataRequired(), validators.Length(min = 1, max = 50)])
    password = PasswordField('password', [validators.DataRequired(), validators.EqualTo('confirm', message = 'Passwords must match')])
    confirm = PasswordField('Repeat Password')
    

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.String(200))
    email = db.Column(db.String(150), unique = True)
    username = db.Column(db.String(150))
    password = db.Column(db.String(150))

    def __init__(self, fullname, email, username, password):
        self.fullname = fullname
        self.email = email
        self.username = username
        self.password = password

# Routes
@app.route("/")
def index():
    return render_template('home.html')


@app.route("/register",  methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():
        user = User(form.fullname.data, form.email.data, form.username.data, form.password.data)
        db.session.add(user)
        flash('Thanks for registering')
        db.session.commit()
        return render_template('login.html')
    
    return render_template('register.html', message="error", form=form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template('login.html')



# App Run
if __name__ == '__main__':
    app.secret_key = 'MYVERYSECRETKEYTHATCANTBEHACKEDLMAO';
    app.run()