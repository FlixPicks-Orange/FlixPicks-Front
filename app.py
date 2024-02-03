from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import os, random

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'database.db')
app.config['SECRET_KEY'] = 'spongebob'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, unique =True)
    username = db.Column(db.String(20), nullable=False, unique = True)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.Integer, default=0)

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder" : "Username"})

    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder" : "Password"})
    
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()

        if existing_user_username:
            raise ValidationError("Username already exits")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder" : "Username"})

    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder" : "Password"})
    
    submit = SubmitField("Login")





@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=['GET' , 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return(redirect(url_for('userhome')))
    return render_template('login.html', form =form)

@app.route('/register', methods=['GET' , 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form = form)

@app.route('/userhome', methods=['GET' , 'POST'])
@login_required
def userhome():
    return render_template('userhome.html')

@app.route('/spin', methods=['POST'])
def spin():
    options = request.form.get('options')
    if not options:
        return "Please enter at least one option."

    options_list = options.split(',')
    selected_option = random.choice(options_list)
    return render_template('result.html', selected_option=selected_option)


@app.route('/result', methods=['POSt'])
def result():
    options = request.form.getlist('option')
    selected_option = random.choice(options)
    return render_template('result.html', selected_option=selected_option)

@app.route('/mediaInfo/<int:page_id>', methods=['GET' , 'POST'])
@login_required
def mediaInfo(page_id):
    return render_template('mediaInfo.html', page_id=page_id)

@app.route('/logout', methods = ['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=2000, debug=True)
