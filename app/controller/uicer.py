from flask import Blueprint, render_template, request, session, g, redirect, url_for
from sqlalchemy import func
from app.models.base import db
from app.models.uicer import Uicer
from app.models.alumni import Alumni
from app.controller.forms import RegistForm, LoginForm,PasswordFrom

uicerBP = Blueprint('uicer',__name__)


@uicerBP.route('/register',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('uicer_register.html', flag=None)
    else:
        form = RegistForm(request.form)
        if form.validate():
            email=form.email.data
            if len(email)>10:
                email = email[:10]
            name = form.name.data
            password = form.password.data
            gpa=request.form.get('gpa')
            gender = request.form.get('gender')
            uicer=Uicer(name, email, password, gpa, gender)
            db.session.add(uicer)
            db.session.commit()
            return render_template('Login.html', message='Register Successfully, backing to Login !')
        else:
            message=form.errors.get('email')
            if message:
                return render_template('uicer_register.html', flag='fail', message=message)
            message = form.errors.get('name')
            if message:
                return render_template('uicer_register.html', flag='fail', message=message)
            message = form.errors.get('password')
            if message:
                return render_template('uicer_register.html', flag='fail', message=message)
            message = form.errors.get('c_password')
            if message:
                return render_template('uicer_register.html', flag='fail', message=message)
            return 'fail'

@uicerBP.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            if len(email)>10:
                email = email[:10]
            password = form.password.data
            uicer = Uicer.query.filter_by(email=email).first()
            if uicer and uicer.check_password(password):
                session['id'] = uicer.id
                # g.uicer = uicer
                return redirect(url_for('uicer.index'))
            else:
                return render_template('login.html', message = 'Wrong Account or Password !')
        else:
            return render_template('login.html')

@uicerBP.route('/logout',methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('uicer.login'))

@uicerBP.route('/',methods=['GET','POST'])
def index():
    if request.method=='GET':
        if g.uicer:
            return render_template('index.html', message="you are uicer. your name is " + g.uicer.name)
        elif g.alumni:
            return render_template('index.html', message="you are alumni. your name is "+g.alumni.name)
        else:
            return render_template('index.html')
    else:
        return "You haven't logged in yet"

@uicerBP.route('/change_password',methods=['GET','POST'])
def change_password():
    if request.method=='GET':
        return render_template('change_password.html')
    else:
        form = PasswordFrom(request.form)
        new_password= form.new_password.data
        if g.alumni:
            user=g.alumni
        elif g.uicer:
            user=g.uicer
        else:
            return redirect(url_for('uicer.index'))
        user.change_password(new_password)
        db.session.commit()
        return redirect(url_for('uicer.index'))

@uicerBP.route('/beAlumni',methods=['GET','POST'])
def beAlumni():
    if request.method=='GET':
        return render_template('beAlumni.html')
    else:
        user = g.uicer
        name = user.name
        email = user.email
        password = user.password
        gpa = user.gpa
        gender = user.gender
        status = request.form.get('status')
        aNFlag = request.form.get('anonymousName')
        if aNFlag:
            anonymousName = True if aNFlag.lower() == 'true' else False
        else:
            anonymousName = False
        db.session.delete(user)
        db.session.commit()
        alumni = Alumni(name, email, password, gpa, gender, status, anonymousName)
        db.session.add(alumni)
        db.session.commit()
        session['id'] = alumni.id
        return redirect(url_for('uicer.index'))

@uicerBP.route('/auto_add',methods=['GET'])
def auto_add():
    # with db.auto_commit():
    #     uicer1 = Uicer('Bob', "q030026100","1234567", 2.8,'male')
    #     uicer2 = Uicer('JoJo', "q030026200","123456", 3.2, 'female')
    #     uicer3 = Uicer('Jam', "q030026300", "123456", 3.5, 'helicopter')
    #     db.session.add(uicer1)
    #     db.session.add(uicer2)
    #     db.session.add(uicer3)
    with db.auto_commit():
        uicer_data = [
            {
                'name': 'Bob',
                'email': 'q030026100',
                'password': '1234567',
                'gpa': 2.8,
                'gender': 'male'
            },
            {
                'name': 'JoJo',
                'email': 'q030026200',
                'password': '123456',
                'gpa': 3.2,
                'gender': 'female'
            },
            {
                'name': 'Jam',
                'email': 'q030026300',
                'password': '123456',
                'gpa': 3.5,
                'gender': 'helicopter'
            },
            {
                'name': 'Alice',
                'email': 'q030026400',
                'password': '987654',
                'gpa': 3.9,
                'gender': 'female'
            },
            {
                'name': 'John',
                'email': 'q030026500',
                'password': 'qwerty',
                'gpa': 3.7,
                'gender': 'male'
            },
            {
                'name': 'Emma',
                'email': 'q030026600',
                'password': 'password',
                'gpa': 3.6,
                'gender': 'female'
            },
            {
                'name': 'David',
                'email': 'q030026700',
                'password': 'pass123',
                'gpa': 2.9,
                'gender': 'male'
            },
            {
                'name': 'Olivia',
                'email': 'q030026800',
                'password': 'abcd1234',
                'gpa': 3.8,
                'gender': 'female'
            },
            {
                'name': 'James',
                'email': 'q030026900',
                'password': 'p@ssw0rd',
                'gpa': 2.5,
                'gender': 'male'
            },
            {
                'name': 'Sophia',
                'email': 'q030027000',
                'password': 'passpass',
                'gpa': 3.3,
                'gender': 'female'
            }
        ]

        for data in uicer_data:
            uicer = Uicer(
                name=data['name'],
                email=data['email'],
                password=data['password'],
                gpa=data['gpa'],
                gender=data['gender']
            )
            db.session.add(uicer)
    return "uicer add successfully"
