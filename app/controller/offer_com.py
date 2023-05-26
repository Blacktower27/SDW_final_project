#controller
from flask import Blueprint, render_template, request,redirect,url_for
from app.models.base import db
from app.models.offer_com import Offer_com
from base64 import b64encode
from datetime import datetime

offer_comBP = Blueprint('offer_comBP', __name__)

@offer_comBP.route('/add', methods=['GET', 'POST'])
def add_offer():
    if request.method == 'GET':
        return redirect(url_for('offer.add_offer'))
    else:
        file = request.files['photoCopy']
        photoCopy = file.read()
        date_str = request.form.get('date')
        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            date = None
        gpa = request.form.get('gpa')
        title = request.form.get('title')
        companyName = request.form.get('companyName')
        employmentExperience = request.form.get('employmentExperience')
        offer_com = Offer_com(date, gpa,photoCopy,title,companyName,employmentExperience)
        db.session.add(offer_com)
        db.session.commit()
        return render_template('index.html',message="company offer add successfully!")