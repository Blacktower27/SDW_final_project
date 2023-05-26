#controller
from operator import and_
from flask import Blueprint, render_template, request
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import false
from app.controller import offer_tac, program
from app.models.base import db
from app.models.offer_tac import Offer_tac
from app.models.program import Program
from app.models.university import University
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

reportBP = Blueprint('report', __name__)

@reportBP.route('/gpa_dis', methods=['GET', "POST"])
def report_gpa_dis():
    if request.method == 'GET':
        return render_template('report_gpa_dis.html')
    else:
        year = int(request.form.get('year'))
        t1 = datetime.datetime(year, 1, 1)
        t2 = datetime.datetime(year + 1, 1, 1)
        offers = Offer_tac.query.filter(and_(Offer_tac.date >= t1, Offer_tac.date < t2)).all()
        gpa_ranges = ['2.0-3.0', '3.0-3.33', '3.33-3.67', '3.67-4.0']
        gpa_counts = [0, 0, 0, 0]
        for o in offers:
            gpa = o.gpa
            if gpa >= 2.0 and gpa < 3.0:
                gpa_counts[0] += 1
            elif gpa >= 3.0 and gpa < 3.33:
                gpa_counts[1] += 1
            elif gpa >= 3.33 and gpa < 3.67:
                gpa_counts[2] += 1
            elif gpa >= 3.67 and gpa <= 4.0:
                gpa_counts[3] += 1

        total_count = sum(gpa_counts)
        if total_count == 0:
            plt.title('GPA Distribution')
            plt.savefig('./app/static/image/gpa_pie_chart.png')
            plt.clf()
        else:
            gpa_percentages = [count/total_count*100 for count in gpa_counts]
            labels = gpa_ranges
            sizes = gpa_percentages
            colors = ['red', 'orange', 'yellow', 'green']
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            plt.title('GPA Distribution')
            plt.savefig('./app/static/image/gpa_pie_chart.png')
            plt.clf()

        return render_template('generate_report_gpa_dis.html', offers = offers)

@reportBP.route('/pro_dis', methods=['GET', "POST"])
def report_pro_dis():
    if request.method == 'GET':
        return render_template('report_pro_dis.html')
    else:
        year = int(request.form.get('year'))
        t1 = datetime.datetime(year, 1, 1)
        t2 = datetime.datetime(year + 1, 1, 1)
        offers = Offer_tac.query.filter(and_(Offer_tac.date >= t1, Offer_tac.date < t2)).all()
        program_name = []
        program_counts = []
        for o in offers:
            p = Program.query.filter(Program.id == o.program_id).first()
            if p.programName in program_name:
                i = program_name.index(p.programName)
                program_counts[i] = program_counts[i] + 1
            else:
                 program_name.append(p.programName)
                 program_counts.append(1)

        total_count = sum(program_counts)
        program_percentages = [count/total_count*100 for count in program_counts]
        labels = program_name
        sizes = program_percentages
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title('Program Distribution')
        plt.savefig("./app/static/image/program_pie_chart.png")
        plt.clf()

        return render_template('generate_report_pro_dis.html', offers = offers)

@reportBP.route('/uni_bar', methods=['GET', "POST"])
def report_uni_bar():
    if request.method == 'GET':
        return render_template('report_uni_bar.html')
    else:
        year = int(request.form.get('year'))
        t1 = datetime.datetime(year, 1, 1)
        t2 = datetime.datetime(year + 1, 1, 1)
        offers = Offer_tac.query.filter(and_(Offer_tac.date >= t1, Offer_tac.date < t2)).all()
        gpa_ranges = ['2.0-3.0', '3.0-3.33', '3.33-3.67', '3.67-4.0']
        gpa_counts = [0, 0, 0, 0]
        program_name = []
        program_counts = []
        university_name = []
        university_counts = []
        for o in offers:
            p = Program.query.filter(Program.id == o.program_id).first()
            u = University.query.filter(University.id == p.university_id).first()
            if u.universityName in university_name:
                i = university_name.index(u.universityName)
                university_counts[i] = university_counts[i] + 1
            else:
                university_name.append(u.universityName)
                university_counts.append(1)

        # university bar chart
        plt.figure(figsize=(10, 10))
        plt.bar(university_name, university_counts)
        plt.title('Number of Admitted Students by Universities')
        plt.xlabel('School')
        plt.ylabel('Number Admitted')
        plt.xticks(rotation = 30, ha = 'right')
        
        plt.savefig('./app/static/image/university_bar_chart.png')
        plt.clf()

        return render_template('generate_report_uni_bar.html', offers = offers)

@reportBP.route('/uni_dis', methods=['GET', "POST"])
def report_uni_dis():
    if request.method == 'GET':
        return render_template('report_uni_dis.html')
    else:
        year = int(request.form.get('year'))
        t1 = datetime.datetime(year, 1, 1)
        t2 = datetime.datetime(year + 1, 1, 1)
        offers = Offer_tac.query.filter(and_(Offer_tac.date >= t1, Offer_tac.date < t2)).all()
        university_name = []
        university_counts = []
        for o in offers:
            p = Program.query.filter(Program.id == o.program_id).first()
            u = University.query.filter(University.id == p.university_id).first()
            if u.universityName in university_name:
                i = university_name.index(u.universityName)
                university_counts[i] = university_counts[i] + 1
            else:
                university_name.append(u.universityName)
                university_counts.append(1)


        #university distribution
        total_count = sum(university_counts)
        university_percentages = [count/total_count*100 for count in university_counts]
        labels = university_name
        sizes = university_percentages
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title('University Distribution')
        plt.savefig('./app/static/image/university_pie_chart.png')
        plt.clf()

        return render_template('generate_report_uni_dis.html', offers = offers)