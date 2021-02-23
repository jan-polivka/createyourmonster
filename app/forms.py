from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, SubmitField

#races=[('dwarf', 'Dwarf'), ('elf', 'Elf'), ('half', 'Halfling'),
#        ('human', 'Human'), ('drag', 'Dragonborn'), ('gnome', 'Gnome'),
#        ('helf', 'Half-Elf'), ('orc', 'Half-Orc'), ('tief', 'Tiefling')]


races=[('dwarf', 'Hill Dwarf'), ('elf', 'High Elf'),
        ('half', 'Lightfoot Halfling'), ('human', 'Human'),
        ('drag', 'Dragonborn'), ('gnome', 'Rock Gnome'),
        ('helf', 'Half-Elf'), ('orc', 'Half-Orc'), ('tief', 'Tiefling')]

#variants = {'dwarf':[('hill', 'Hill Dwarf')], 'elf':[('high', 'High Elf')]}

classes=[('barbarian', 'Barbarian'), ('bard', 'Bard')]

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

class ClassDets(FlaskForm):
    classList = []
    submit = SubmitField('Next')

    def addLevels(self, number):
        for i in range(number):
            self.classList.append(SelectField('Class', choices=classes))


#class SkillsLangsDets(FlaskForm):

