from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, FieldList, FormField, \
                PasswordField, StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User

#races=[('dwarf', 'Dwarf'), ('elf', 'Elf'), ('half', 'Halfling'),
#        ('human', 'Human'), ('drag', 'Dragonborn'), ('gnome', 'Gnome'),
#        ('helf', 'Half-Elf'), ('orc', 'Half-Orc'), ('tief', 'Tiefling')]


races=[('dwarf', 'Hill Dwarf'), ('elf', 'High Elf'),
        ('half', 'Lightfoot Halfling'), ('human', 'Human'),
        ('drag', 'Dragonborn'), ('gnome', 'Rock Gnome'),
        ('helf', 'Half-Elf'), ('orc', 'Half-Orc'), ('tief', 'Tiefling')]

#variants = {'dwarf':[('hill', 'Hill Dwarf')], 'elf':[('high', 'High Elf')]}

classes=[('barbarian', 'Barbarian'), ('bard', 'Bard')]

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
    race = SelectField('Race', choices=races)
#    variants = SelectField('Race', coerce=str)
    gender = StringField('Gender')
    background = StringField('Background')
    alignment = StringField('Alignment')
    deity = StringField('Deity')
    pt1 = StringField('Personality Trait 1')
    pt2 = StringField('Personality Trait 2')
    ideal = StringField('Ideal')
    bond = StringField('Bond')
    flaw = StringField('Flaw')
    level = IntegerField('Level')
    submit = SubmitField('Next')

class singleClass(FlaskForm):
    classPick = SelectField('Class', choices=classes)
    hitPoints = IntegerField('Hit Points')

class ClassDets(FlaskForm):
    submit = SubmitField('Next')
    classList = FieldList(FormField(singleClass))


#class SkillsLangsDets(FlaskForm):

