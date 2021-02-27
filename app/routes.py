from flask import render_template, redirect, request, session
from app import app
from app.forms import CharDets, ClassDets, classes, singleClass
from wtforms import IntegerField, FormField, SelectField

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', title = 'Home')

@app.route('/charDet.html', methods=['GET','POST'])
def charDet():
        form = CharDets()
        if form.validate_on_submit():
            session['level'] = form.level.data
            return redirect('/classDet.html')
        return render_template('charDet.html', title='New Character',
                form = form)

@app.route('/classDet.html', methods=['GET','POST'])
def classDet():
    form = ClassDets()
    for i in range(session['level']):
        form.classList.append_entry(FormField(singleClass))
    return render_template('classDet.html', title='New Character',
            form = form, length = session['level'])

#@app.route('/skillsDet.html', methods=['GET','POST'])
#def skillsLangDet():


