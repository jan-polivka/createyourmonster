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

languages = [('Common')]

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
    acrobatics = SelectField('Acrobatic', choice=skills)
    animals = SelectField('Animal Handling', choice=skills)
    arcana = SelectField('Arcana', choice=skills)
    athletics = SelectField('Athletics', choice=skills)
    deception = SelectField('Deception', choice=skills)
    history = SelectField('History', choice=skills)
    insight = SelectField('Insight', choice=skills)
    intimidation = SelectField('Intimidation', choice=skills)
    investigation = SelectField('Investigation', choice=skills)
    medicine = SelectField('Medicine', choice=skills)
    nature = SelectField('Nature', choice=skills)
    perception = SelectField('Perception', choice=skills)
    performance = SelectField('Performance', choice=skills)
    persuasion = SelectField('Persuasion', choice=skills)
    religion = SelectField('Religion', choice=skills)
    sleight = SelectField('Sleight of Hand', choice=skills)
    stealth = SelectField('Stealth', choice=skills)
    survival = SelectField('Survival', choice=skills)
