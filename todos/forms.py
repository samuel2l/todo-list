from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from todos.models import User


class RegisterForm(FlaskForm):

    def validate_email(self, email_check):
        email = User.query.filter_by(email=email_check.data).first()
        if email:
            raise ValidationError("User with email already exists")

    name = StringField(label='Your name', validators=[Length(min=1, max=600), DataRequired()])
    email = StringField(label='email', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label="Create Account")


class LoginForm(FlaskForm):
    email = StringField(label='enter email', validators=[Email(), DataRequired()])
    password = PasswordField(label='enter password', validators=[DataRequired()])
    submit = SubmitField(label="Log in")


class NewTodoForm(FlaskForm):
    title = StringField(label='enter title', validators=[DataRequired()])
    content = TextAreaField(label='enter content')
    submit = SubmitField(label="Add todo")


class DelForm(FlaskForm):
    submit = SubmitField(label="Delete todo")


class UpdateForm(FlaskForm):
    title = StringField(label='enter title', validators=[DataRequired()])
    content = TextAreaField(label='enter content')
    submit = SubmitField(label="Update todo")
