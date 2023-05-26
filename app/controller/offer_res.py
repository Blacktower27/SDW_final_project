#controller
from flask import Blueprint, render_template, request,redirect,url_for
from app.models.base import db
from app.models.offer_res import Offer_res
from base64 import b64encode
from datetime import datetime
from app.models.program import Program
from app.models.university import University

offer_resBP = Blueprint('offer_resBP', __name__)

@offer_resBP.route('/add', methods=['GET', 'POST'])
def add_offer():
    if request.method == 'GET':
        return redirect(url_for('offer.add_offer'))
    else:
        file = request.files['photoCopy']
        photoCopy = file.read()
        supervisor = request.form.get('supervisor')
        name = request.form.get('name')
        reseachtopic = request.form.get('reseachtopic')
        Nopaper = request.form.get('Nopaper')
        Noreach = request.form.get('Noreach')
        date_str = request.form.get('date')
        programName = request.form.get('programName')
        universityName = request.form.get('universityName')
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
            offer_res = Offer_res(date, gpa, photoCopy,supervisor,name,reseachtopic,Nopaper,Noreach)
            offer_res.program=program
            db.session.add(offer_res)
            db.session.commit()
            return render_template('index.html',message="research offer add successfully!")
        else:
            return render_template('add_offer.html', message='there is no such program, try again.')

@offer_resBP.route('/view',methods=['POST'])
def view_offer_res():
    universityName = request.form.get('universityName')
    programName = request.form.get('programName')
    program = Program.query.filter_by(programName=programName, university=University.query.filter_by(
        universityName=universityName).first()).first()
    year = request.form.get('year')
    if program:
        offer_ress = Offer_res.query.filter_by(program=program).order_by(Offer_res.date).all()
        if offer_ress:
            unique_years = set()
            for offer_res in offer_ress:
                unique_years.add(offer_res.date.year)
            years = list(unique_years)
            if year == None or year == 'data':
                return render_template('view_offer_res.html', offer_ress=offer_ress, message=None, years=years,
                                       universityName=universityName, programName=programName)
            else:
                year = int(year)
                t1 = datetime(year, 1, 1)
                t2 = datetime(year + 1, 1, 1)
                offer_ress = Offer_res.query.filter(Offer_res.date >= t1, Offer_res.date < t2).filter_by(
                    program=program).order_by(Offer_res.date).all()
                return render_template('view_offer_res.html', offer_ress=offer_ress, message=None, years=years,
                                       universityName=universityName, programName=programName)
        else:
            return render_template('view_offer_res.html', offer_ress=None,
                                   message='there is no such information from alumni')
    else:
        return render_template('view_offer_res.html', offer_ress=None,
                               message='there is no such program with university')