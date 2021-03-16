from flask import flash, render_template, redirect, request, session, \
                    url_for
from flask_login import current_user, login_user, logout_user
from app import app, db
from app.models import Sheet, User
from app.forms import CharDets, ClassDets, languages, LoginForm, \
                        RegistrationForm, skills, \
                        SkillsLangsDets, SingleClass, SingleLang
from wtforms import IntegerField, FormField, SelectField

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', title = 'Home')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('/index.html'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrats, you\'re registered!')
        return redirect('/login')
    return render_template('register.html', title = 'Register',
                                                            form = form)

@app.route('/charDet.html', methods=['GET','POST'])
def charDet():
        form = CharDets()
        if form.validate_on_submit():
            session['level'] = form.level.data
            if current_user.is_authenticated:
                #One could certainly make an argument that accessing
                #the database before the sheet creation is finished
                #is not a good solution and I agree.
                #I think the creation would be best handled client-side
                #until the final submission.
                #Data handling on the client-side is outside the scope
                #of this side-project and therefore I am okay with
                #such short-comings as this.
                s = Sheet(user_id=current_user.get_id(),
                        name=form.name.data,
                        gender=form.gender.data,
                        level=form.level.data)
                db.session.add(s)
                db.session.commit()
            return redirect(url_for('classDet'))
        return render_template('charDet.html', title='New Character',
                form = form)

@app.route('/classDet.html', methods=['GET','POST'])
def classDet():
    form = ClassDets()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            user = User.query.get(current_user.get_id())
            user.sheets[-1].hitPoints = 0
            user.sheets[-1].barbarian = 0
            user.sheets[-1].bard = 0
            for el in form.classList:
                user.sheets[-1].hitPoints += el.data['hitPoints']
                if el.data['classPick'] == "barbarian":
                    user.sheets[-1].barbarian += 1
                elif el.data['classPick'] == "bard":
                    user.sheets[-1].bard += 1
            db.session.commit()
        return redirect(url_for('skillsLangDet'))
    for i in range(session['level']):
        form.classList.append_entry(FormField(SingleClass))
    return render_template('classDet.html', title='New Character',
            form = form, length = session['level'])

@app.route('/skillsDet.html', methods=['GET','POST'])
def skillsLangDet():
    form = SkillsLangsDets()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            user = User.query.get(current_user.get_id())
            for el in form.langList:
                if el.data['lang'] == 'Common':
                    user.sheets[-1].common = True
                if el.data['lang'] == 'Dwarvish':
                    user.sheets[-1].dwarvish = True
                if el.data['lang'] == 'Elvish':
                    user.sheets[-1].elvish = True
            user.sheets[-1].acrobatics = skills.index(form.acrobatics.data)
            user.sheets[-1].animals = skills.index(form.animals.data)
            user.sheets[-1].arcana = skills.index(form.arcana.data)
            db.session.commit()
        return redirect(url_for('index'))
    #Because I am creating a proof of concept, I decided to use
    #an arbitrary number for the number of languages
    MAGIC_NUMBER = 3 
    for i in range(MAGIC_NUMBER):
        form.langList.append_entry(FormField(SingleLang))
    return render_template('skillsLangsDet.html', title='New Character',
            form=form)

@app.route('/characters.html')
def charView():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        us_id = current_user.get_id()
        char = User.query.get(us_id)
        lst = char.sheets.all()
        return render_template('characters.html',
                title = 'Your characters', lst = lst)

@app.route('/delChar/<char_id>')
def delChar(char_id):
    sheet = Sheet.query.get(char_id)
    if sheet.user_id == int(current_user.get_id()):
        db.session.delete(sheet)
        db.session.commit()
        return redirect(url_for('charView'))
    else:
        return redirect('/chars/'+str(sheet.id))

@app.route('/editChar/<char_id>', methods = ['GET','POST'])
def editChar(char_id):
    sheet = Sheet.query.get(char_id)
    form = CharDets(name = sheet.name, gender = sheet.gender,
            level = sheet.level)
    if sheet.user_id != int(current_user.get_id()):
        return redirect(url_for('index'))
    attributes = ['name', 'gender', 'level']

    if form.validate_on_submit():
        for attr in attributes:
            setattr(sheet, attr, getattr(form, attr).data)
        db.session.commit()
        return redirect('/chars/'+str(sheet.id))
    return render_template('editChar.html', title = 'Edit you character',
            form = form)

#@app.route('/editClass/<char_id>', methods = ['GET','POST'])
#def editClass(char_id):
#    sheet = Sheet.query.get(char_id)
#    form = ClassDets(name = sheet.name, gender = sheet.gender,
#            level = sheet.level)
#    if sheet.user_id != int(current_user.get_id()):
#        return redirect(url_for('index'))
#    attributes = ['name', 'gender', 'level']
#
#    if form.validate_on_submit():
#        for attr in attributes:
#            setattr(sheet, attr, getattr(form, attr).data)
#        db.session.commit()
#        return redirect('/chars/'+str(sheet.id))
#    return render_template('editClass.html', title = 'Edit you character',
#            form = form)


#@app.route('/editSkills/<char_id>', methods = ['GET','POST'])
#def editSkills(char_id):

@app.route('/chars/<char_id>')
def singleChar(char_id):
    sheet = Sheet.query.get(char_id)
    langList = []
    langs = (languages[1:])
    for lang in langs:
        if getattr(sheet, lang.lower()):
            langList.append(lang)
    profList = []
    expList = []
    for skill in ['Acrobatics', 'Animals', 'Arcana']:
        if getattr(sheet, skill.lower()) == 1:
            profList.append(skill)
        if getattr(sheet, skill.lower()) == 2:
            expList.append(skill)
    classList = []
    if sheet.barbarian:
        classList.append('Barbarian, level {}'.format(sheet.barbarian))
    if sheet.bard:
        classList.append('Bard, level {}'.format(sheet.bard))
    return render_template('singleChar.html', title = 'Your char',
            sheet = sheet, langList = langList, profList = profList,
            expList = expList, classList = classList)
