from flask import flash, render_template, redirect, request, session, \
                    url_for
from flask_login import current_user, login_user, logout_user
from app import app, db
from app.models import Sheet, User
from app.forms import CharDets, ClassDets, LoginForm, \
                        RegistrationForm, \
                        SkillsLangsDets, SingleClass
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
        user = User(username = form.username.data, email = "x@y.cz")
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
                s = Sheet(user_id=current_user.get_id(),
                        name=form.name.data,
                        gender=form.gender.data,
                        level=form.level.data)
                db.session.add(s)
                db.session.commit()
                print (Sheet.query.all())
            return redirect(url_for('classDet'))
        return render_template('charDet.html', title='New Character',
                form = form)

@app.route('/classDet.html', methods=['GET','POST'])
def classDet():
    form = ClassDets()
    if form.validate_on_submit():
        print ("redirect?")
        return redirect(url_for('skillsLangDet'))
    for i in range(session['level']):
        form.classList.append_entry(FormField(SingleClass))
    print ("retting")
    print (form.errors)
    return render_template('classDet.html', title='New Character',
            form = form, length = session['level'])

@app.route('/skillsDet.html', methods=['GET','POST'])
def skillsLangDet():
    form = SkillsLangsDets()
    if form.validate_on_submit():
        return redirect(url_for('index'))
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
