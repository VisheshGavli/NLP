from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import Email, DataRequired, Length, EqualTo, ValidationError
from blog.models import User

class RegistrationForm(FlaskForm):

    username = StringField(_name='Username',validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField(_name='Email', validators=[DataRequired(),Email()])
    password = PasswordField(_name='Password', validators=[DataRequired(),Length(min=6)])
    confirm_password = PasswordField(_name='Confirm Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField(_name='Register')

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already exists. Pls choose a different one.")

    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exists. Pls choose a different one.")

class LoginForm(FlaskForm):

    email = StringField(_name='Email', validators=[DataRequired(),Email()])
    password = PasswordField(_name='Password', validators=[DataRequired()])
    remember = BooleanField(_name='Remember Me')
    login = SubmitField(_name='Login')
