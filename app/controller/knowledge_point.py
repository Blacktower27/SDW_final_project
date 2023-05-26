from flask import Blueprint, render_template, request, g, redirect, url_for
from sqlalchemy import func
from app.models.base import db
from app.models.knowledge_point import Knowledge_point as KP
from app.controller.forms import RegistForm
from app.models.program import Program
from app.models.alumni import Alumni
from app.models.university import University
from app.models.knowledge_point import Knowledge_point

kpBP = Blueprint('knowledge_point',__name__)

@kpBP.route('/auto_add',methods=["get"])
def auto_add():
    kp1=KP("lesson1 lesson2 lesson3")
    kp1.program =Program.query.get(1)
    kp1.alumni = Alumni.query.get(1)
    kp2 = KP("lesson2 lesson2 lesson4")
    kp2.program = Program.query.get(2)
    kp2.alumni = Alumni.query.get(2)
    db.session.add(kp1)
    db.session.add(kp2)
    db.session.commit()
    return "add knowledge points successfully"

@kpBP.route('/add', methods=['GET','POST'])
def kp_add():
    alumni=g.alumni
    if alumni:
        if request.method=='GET':
            return render_template('kp_add.html')
        else:
            programName = request.form.get('programName')
            universityName = request.form.get('universityName')
            courseNameList = request.form.get('courseNameList')
            # university = University.query.filter_by(universityName=universityName).first()
            program = Program.query.filter_by(programName=programName, university=University.query.filter_by(
                universityName=universityName).first()).first()
            if program:
                kp = Knowledge_point(courseNameList)
                kp.program=program
                kp.alumni = alumni
                db.session.add(kp)
                db.session.commit()
                return redirect(url_for('uicer.index'))
            else:
                return render_template('add_university.html', flag='fail', message='No such program with university')
    else:
        return redirect(url_for('uicer.index'))

@kpBP.route('/view',methods=['GET','POST'])
def view_kp():
    if request.method=='GET':
        return render_template('view_kp.html')
    else:
        programName = request.form.get('programName')
        universityName = request.form.get('universityName')
        program = Program.query.filter_by(programName=programName, university=University.query.filter_by(
            universityName=universityName).first()).first()
        if program:
            kps = Knowledge_point.query.filter_by(program=program)
            if kps:
                return render_template('view_kp.html', kps=kps)
            else:
                return render_template('view_kp.html', kps=None, message='Alumni have not provide the information')
        else:
            return render_template('view_kp.html', flag='fail', message='no such program with university')

