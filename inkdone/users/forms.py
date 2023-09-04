from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField, BooleanField
from wtforms.validators import Length, DataRequired, ValidationError, EqualTo
from inkdone.users.models import User
from flask_login import current_user


class SignUpForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email(self, email_address_to_check):
        email_address = User.query.filter_by(email=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')
        
    username = StringField(label='Username:', validators=[Length(min=3, max=80), DataRequired()])
    email = EmailField(label='Email:', validators=[Length(max=120), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=3), DataRequired()])
    password2 = PasswordField(label='Confirm password:', validators=[EqualTo('password1', message='Passwords do not match.'), DataRequired()])
    submit = SubmitField(label='Submit')


class LoginForm(FlaskForm):
        
    username = StringField(label='Username:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Submit')
    

class ProfileEditForm(FlaskForm):

    def validate_email(self, email_address_to_check):
        if email_address_to_check.data != current_user.email:
            email_address = User.query.filter_by(email=email_address_to_check.data).first()
            if email_address:
                raise ValidationError('Email Address already exists! Please try a different email address')
            
    email = EmailField(label='Email:', validators=[Length(max=120), DataRequired()])
    bio = TextAreaField(label='Bio:', validators=[Length(max=1000)])
    image = FileField(label='Picture', validators=[FileAllowed(['jpg', 'png'])])
    clear_image = BooleanField(label='Remove Image:')
    academics = TextAreaField(label='Academics:', validators=[Length(max=1500)])
    accomplishment_name = StringField(label='Accomplishment:', validators=[Length(max=50)])
    accomplishment_description = TextAreaField(label='Description:', validators=[Length(max=3000)])
    
    submit = SubmitField(label='Submit')