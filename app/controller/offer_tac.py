#controller
from flask import Blueprint, render_template, request,redirect,url_for
from app.models.base import db
from app.models.offer_tac import Offer_tac
from app.models.offer_res import Offer_res
from datetime import datetime
from app.models.program import Program
from app.models.university import University

offer_tacBP = Blueprint('offer_tacBP', __name__)

@offer_tacBP.route('/add', methods=['GET', 'POST'])
def add_offer():
    if request.method == 'GET':
        return redirect(url_for('offer.add_offer'))
    else:
        file = request.files['photoCopy']
        photoCopy = file.read()
        programName = request.form.get('programName')
        universityName = request.form.get('universityName')
        date_str = request.form.get('date')
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            date = None
        gpa = float(request.form.get('gpa'))
        program = Program.query.filter_by(programName=programName, university=University.query.filter_by(
            universityName=universityName).first()).first()
        if program:
            if gpa<program.gpaLow:
                program.gpaLow=gpa
            if gpa>program.gpaHigh:
                program.gpaHigh=gpa
            offer_tac = Offer_tac(date, gpa, photoCopy)
            offer_tac.program=program
            db.session.add(offer_tac)
            db.session.commit()
            return render_template('add_offer.html', message = 'Taught offer add successfully.')
        else:
            return render_template('add_offer.html', message = 'There is no such program or university, please add the new program and university !')
@offer_tacBP.route('view',methods=["post"])
def view_offer_tac():
    universityName=request.form.get('universityName')
    programName = request.form.get('programName')
    program = Program.query.filter_by(programName=programName, university=University.query.filter_by(
        universityName=universityName).first()).first()
    year = request.form.get('year')
    if program:
        offer_tacs = Offer_tac.query.filter_by(program=program).order_by(Offer_tac.date).all()
        if offer_tacs:
            unique_years = set()
            for offer_tac in offer_tacs:
                unique_years.add(offer_tac.date.year)
            years = list(unique_years)
            if year == None or year == 'data':
                return render_template('view_offer_tac.html', offer_tacs=offer_tacs, message=None,years=years,universityName=universityName,programName=programName)
            else:
                year=int(year)
                t1 = datetime(year, 1, 1)
                t2 = datetime(year + 1, 1, 1)
                offer_tacs = Offer_tac.query.filter(Offer_tac.date >= t1, Offer_tac.date < t2).filter_by(program=program).all()
                return render_template('view_offer_tac.html', offer_tacs=offer_tacs, message=None, years=years,
                                       universityName=universityName, programName=programName)
        else:
            return render_template('view_offer_tac.html', offer_tacs=None, message='there is no such information from alumni')
    else:
        return render_template('view_offer_tac.html', offer_tacs=None,
                               message='there is no such program with university')