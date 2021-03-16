from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, FieldList, FormField, \
                PasswordField, StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User

classes=[('barbarian', 'Barbarian'), ('bard', 'Bard')]

languages = [(''), ('Common'), ('Elvish'), ('Dwarvish')]

skills = [(''), ('Proficient'), ('Expertise')]

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    password2 = PasswordField('Repeat Password',
                    validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')
    
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address')


class CharDets(FlaskForm):
    name = StringField('Character Name')
    gender = StringField('Gender')
    level = IntegerField('Level')
    submit = SubmitField('Next')

class SingleClass(FlaskForm):
    classPick = SelectField('Class', choices=classes)
    hitPoints = IntegerField('Hit Points')

class ClassDets(FlaskForm):
    submit = SubmitField('Next')
    classList = FieldList(FormField(SingleClass))

class SingleLang(FlaskForm):
    lang = SelectField('Language', choices=languages)

class SkillsLangsDets(FlaskForm):
    submit = SubmitField('Finish')
    langList = FieldList(FormField(SingleLang))
    acrobatics = SelectField('Acrobatic', choices=skills)
    animals = SelectField('Animal Handling', choices=skills)
    arcana = SelectField('Arcana', choices=skills)
