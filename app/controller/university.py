from flask import Blueprint, render_template, request, jsonify
from sqlalchemy import func
from app.models.base import db
from app.models.university import University
from app.models.program import Program

universityBP = Blueprint('university',__name__)

@universityBP.route('/auto_add',methods=['GET'])
def auto_add():
    with db.auto_commit():
        universities=[
            University('Stanford University'),
            University('Massachusetts Insitute of Technology'),
            University('University of Oxford'),
            University('University of Cambridge'),
            University('Harvard University'),
            University('California Institute of Technology')
        ]
        for university in universities:
            db.session.add(university)
    return "Success add university"

@universityBP.route('/add', methods=['GET','POST'])
def add_university():
    if request.method == 'GET':
        return render_template('add_university.html')
    else :
        universityName = request.form.get('universityName')
        varify = University.query.filter_by(universityName=universityName).first()
        if varify == None:
            university = University(universityName)
            db.session.add(university)
            db.session.commit()
            return render_template('add_university.html', message = 'University Add Successfully !')
        else:
            return render_template('add_university.html', message = 'University Already Exists !')


@universityBP.route('/delete',methods=['GET','POST'])
def delete_university():
    if request.method=='GET':
        return render_template('delete_university.html', message=None)
    else:
        universityName = request.form.get('universityName')
        university= University.query.filter_by(universityName=universityName).first()
        if university:
            programs=Program.query.filter_by(university=university).all()
            db.session.delete(university)
            for program in programs:
                db.session.delete(program)
            db.session.commit()
            return "delete successfully !"
        else:
            return render_template('delete_university.html', message='fail')

@universityBP.route('/searchByUniversity',methods=['GET','POST'])
def searchByUniversity():
    if request.method=='GET':
        return render_template('searchByUniversity.html')
    else:
        universityName = request.form.get('universityName')
        major = request.form.get('major')
        # programName = request.form.get('programName')
        query = db.session.query(Program).join(Program.university)
        # program = query.filter(Program.programName == programName, University.universityName == universityName).first()
        programs = query.filter(University.universityName == universityName).all()
        majors = []
        for program in programs:
            tmajor = program.major
            if tmajor not in majors:
                majors.append(tmajor)
        if major == 'All major' or major == None:
            if programs:
                return render_template('searchByUniversity.html', programs=programs, flag=None, message=None, majors=majors,
                                       universityName=universityName)
            else:
                return render_template('searchByUniversity.html', programs=programs, flag='fail',
                                       message='No program in this university')
        else:
            programs = query.filter(University.universityName == universityName, Program.major==major).all()
            if programs:
                return render_template('searchByUniversity.html', programs=programs, flag=None, message=None, majors=majors,
                                       universityName=universityName)
            else:
                return render_template('searchByUniversity.html', programs=None, flag='fail',
                                       message='No program in this university')

@universityBP.route('/search')
def search():
    keyword = request.args.get('keyword')

    # 根据关键词进行查询和筛选
    suggestions = performSearch(keyword)
    # 返回查询结果
    response = {
        'suggestions': suggestions
    }
    return jsonify(response)

def performSearch(keyword):
    # 根据关键词进行查询和筛选的逻辑
    # 返回一个包含联想搜索结果的列表
    # 例如：根据关键词查询数据库或其他数据源

    # 这里只是一个示例，返回一个静态的联想搜索结果列表
    universityNames=[]
    universities = University.query.all()
    for university in universities:
        universityNames.append(university.universityName)
    filteredSuggestions = [s for s in universityNames if keyword.lower() in s.lower()]

    return filteredSuggestions
# @universityBP.route('/programs',methods=['GET'])
# def show_programs():
#     university = University.query.get(2)
#     for program in university.programs:
#         print(program.GpaLow)
#     return "Success show programs"