from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import os

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
        login_user(new_user)
        return redirect(url_for('tasteProfile'))
    return render_template('register.html', form=form)

@app.route('/tasteProfile', methods=['GET','POST'])
def tasteProfile():
    if request.method== 'POST':
        return redirect(url_for('thank_you'))
    else:
        questions = {
    "What are your favorite genres?":["Horror","Fantasy","Action","Drama","Comedy","Other"],
    "When do you watch TV?":["In the morning, while eating breakfast","In the afternoon, during lunch","At night, after work"],
    "Do you prefer light-hearted movies or more serious ones?": ["Light-hearted","Serious and dramatic"],
    "Live Action or Animation?":["Live Action","Animation"],
    "Do you like a quick binge or to take your time?":["Quick binge","Take my time"],
    "What do you pay attention to most in movies?":["The acting","The plot","Everything"],
    "Who do you typically watch TV with?":["By myself","With friends","With family"],
    "How often to you watch movies?":["Hardly at all","Rarley","Time to Time","Almost every day"],
    "Why do you watch TV?":["To keep up with trending media","To relax","To relieve boredem"],
    "What is your go-to streaming service?":["Netflix","Hulu","MAX","Prime Video","Paramount+","Other"]
        #Add more questions here if needed
}
    return render_template('tasteProfile.html', questions=questions)

@app.route('/thank_you')
@login_required
def thank_you():
    return render_template('thank_you.html')

@app.route('/userhome', methods=['GET' , 'POST'])
@login_required
def userhome():
    return render_template('userhome.html')

@app.route('/mediaInfo', methods=['GET' , 'POST'])
@login_required
def mediaInfo():
    return render_template('mediaInfo.html')

@app.route('/logout', methods = ['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)