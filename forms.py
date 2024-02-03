from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
import users


class RegisterForm(FlaskForm):
    email = EmailField(validators=[InputRequired()], render_kw={"placeholder" : "E-mail Address"})
    fname = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder" : "First Name"})
    lname = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder" : "Last Name"})
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder" : "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder" : "Password"})
    confirm = PasswordField(validators=[InputRequired(), EqualTo('password', 'Password mismatch')], render_kw={"placeholder" : "Confirm Password"})
    submit = SubmitField("Register")
    
    def validate_email(self, email):
        if users.email_exists(email.data):
            raise ValidationError("This E-mail Address is already in use.")
    
    def validate_username(self, username):
        if users.username_exists(username.data):
            raise ValidationError("This username is already in use.")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder" : "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder" : "Password"})
    submit = SubmitField("Login")