from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import func
from app.models.base import db
from app.models.alumni import Alumni
from app.controller.forms import RegistForm

alumniBP = Blueprint('alumni',__name__)


@alumniBP.route('/register',methods=['POST'])
def alumni_register():
    form = RegistForm(request.form)
    if form.validate():
        email = form.email.data
        if len(email) > 10:
            email = email[:10]
        name = form.name.data
        password = form.password.data
        gpa = request.form.get('gpa')
        status = request.form.get('status')
        gender = request.form.get('gender')
        aNFlag = request.form.get('anonymousName')
        if aNFlag:
            anonymousName = True if aNFlag.lower() == 'true' else False
        else:
            anonymousName=False
        alumni = Alumni(name, email, password, gpa, gender, status,anonymousName)
        db.session.add(alumni)
        db.session.commit()
        return redirect(url_for('uicer.index', message = "register success"))
    else:
        message = form.errors.get('email')
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

@alumniBP.route('/update',methods=['GET','POST'])
def update():
    return 'alumni update'

@alumniBP.route('/auto_add',methods=['GET'])
def auto_add():
    # with db.auto_commit():
    #     alumni1 = Alumni('Bob', "q030027900","123456", 2.8, 'Male',"graduate", False)
    #     alumni2 = Alumni('JoJo', "q030027901","123456", 2.8, 'Female', "work", True)
    #     db.session.add(alumni1)
    #     db.session.add(alumni2)
    with db.auto_commit():
        alumni_data = [
            ('Bob', 'q030027900', '123456', 2.8, 'Male', 'graduate', False),
            ('JoJo', 'q030027901', '123456', 2.8, 'Female', 'work', True),
            ('Alice', 'q030027902', '123456', 3.2, 'Female', 'work', False),
            ('John', 'q030027903', '123456', 3.5, 'Male', 'graduate', True),
            ('Emma', 'q030027904', '123456', 3.8, 'Female', 'work', False),
            ('Tom', 'q030027905', '123456', 3.6, 'Male', 'graduate', True),
            ('Lily', 'q030027906', '123456', 2.9, 'Female', 'work', True),
            ('Sam', 'q030027907', '123456', 3.1, 'Male', 'graduate', False),
            ('Sophia', 'q030027908', '123456', 3.3, 'Female', 'work', False),
            ('Daniel', 'q030027909', '123456', 3.7, 'Male', 'graduate', True),
        ]

        for data in alumni_data:
            alumni = Alumni(*data)
            db.session.add(alumni)

    return "Alumini add successfully"