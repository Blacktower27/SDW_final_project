from flask import Blueprint, render_template, request, redirect, jsonify
import json
from app.models.base import db
from app.models.program import Program
from app.models.university import University

programBP = Blueprint('program',__name__)


@programBP.route('/add', methods=['GET','POST'])
def add_program():
    universities = University.query.all()
    if request.method=='GET':
        return render_template('add_program.html',universities=universities,flag=None, message=None)
    else:
        universities = University.query.all()
        programName = request.form.get('programName')
        university_id = request.form.get('university_id')
        university = University.query.get(university_id)
        varify = Program.query.filter_by(programName=programName,university=university).first()
        if varify==None:
            gpaLow = request.form.get('gpaLow')
            gpaHigh = request.form.get('gpaHigh')
            major = request.form.get('major')
            if gpaHigh < gpaLow:
                return render_template('add_program.html', universities=universities, flag='fail',
                                       message='The GPA is invalid')
            program = Program(programName, gpaLow,gpaHigh,major)
            program.university=university
            db.session.add(program)
            db.session.commit()
            return render_template('add_program.html', universities=universities, message = 'Add program successfully !')
        else:
            return render_template('add_program.html', universities=universities, message = 'Program Already Exists !')

@programBP.route('delete', methods=['GET','POST'])
def delete_program():
    universities = University.query.all()
    if request.method=='GET':
        return render_template('delete_program.html',universities=universities,flag=None, message=None)
    else:
        programName = request.form.get('programName')
        university_id = request.form.get('university_id')
        university = University.query.get(university_id)
        program = Program.query.filter_by(programName=programName, university=university).first()
        if program:
            db.session.delete(program)
            db.session.commit()
            return 'Delete program'
        else:
            return render_template('delete_program.html', universities=universities, flag='fail', message='No such program')


@programBP.route('/searchByGPA',methods=['GET','POST'])
def searchByGPA():
    if request.method == 'GET':
        return render_template('searchByGPA.html')
    else:
        major = request.form.get('major')
        gpa = float(request.form.get('gpa'))
        programs = Program.query.filter(Program.gpaLow.isnot(None), Program.gpaHigh.isnot(None)).filter(
            Program.gpaLow > gpa - 1,
            Program.gpaHigh < gpa + 0.5).all()
        majors = []
        for program in programs:
            tmajor = program.major
            if tmajor not in majors:
                majors.append(tmajor)
        if major == 'All major' or major == None:
            if programs:
                return render_template('searchByGPA.html', programs=programs, flag=None, message=None, majors=majors,
                                       gpa=gpa)
            else:
                return render_template('searchByGPA.html', programs=programs, flag='fail',
                                       message='No program around this GPA')
        else:
            programs = Program.query.filter(Program.gpaLow.isnot(None), Program.gpaHigh.isnot(None),
                                            Program.major.isnot(None)).filter(Program.gpaLow > gpa - 1,
                                                                              Program.gpaHigh < gpa + 0.5,
                                                                              Program.major == major).all()
            if programs:
                return render_template('searchByGPA.html', programs=programs, flag=None, message=None, majors=majors,gpa=gpa)
            else:
                return render_template('searchByGPA.html', programs=None, flag='fail',message='No program around this GPA')

@programBP.route('/update', methods=['GET','POST'])
def update():
    if request.method=='GET':
        return render_template('uptate_program.html')
    else:
        # id = request.form.get('id')#正常情况下获取id
        # program = Program.query.get(id)
        programName= request.form.get('programName')
        program= Program.query.filter_by(programName=programName).first()
        if program:
            gpaLow = request.form.get('gpaLow')
            gpaHigh = request.form.get('gpaHigh')
            program.update(gpaLow=gpaLow,gpaHigh=gpaHigh)
            db.session.commit()
            return render_template('uptate_program.html')
        else:
            return 'No such program'

@programBP.route('/search')
def search():
    keyword2 = request.args.get('keyword1')
    keyword1 = request.args.get('keyword2')
    # 根据关键词进行查询和筛选
    suggestions = performSearch(keyword1,keyword2)
    # 返回查询结果
    response = {
        'suggestions': suggestions
    }
    return jsonify(response)

def performSearch(keyword1,keyword2):
    # 根据关键词进行查询和筛选的逻辑
    # 返回一个包含联想搜索结果的列表
    # 例如：根据关键词查询数据库或其他数据源

    # 这里只是一个示例，返回一个静态的联想搜索结果列表
    print(keyword1)
    programNames=[]
    programs = Program.query.filter(Program.university.has(universityName=keyword1)).all()
    print(programs)
    for program in programs:
        programNames.append(program.programName)
    filteredSuggestions = [s for s in programNames if keyword2.lower() in s.lower()]

    return filteredSuggestions

@programBP.route('/auto_add',methods=['GET'])
def auto_add():
    with db.auto_commit():
        program_data = [
            {
                'programName': 'Computer Science',
                'gpaLow' : 3.5,
                'gpaHigh' : 4,
                'major': 'Software Engineering',
                'university_id': 1
            },
            {
                'programName': 'Business Administration',
                'gpaLow' : 3.2,
                'gpaHigh' : 3,
                'major': 'Marketing',
                'university_id': 2
            },
            {
                'programName': 'Mechanical Engineering',
                'gpaLow' : 3.0,
                'gpaHigh' : 4,
                'major': 'Robotics',
                'university_id': 1
            },
            {
                'programName': 'Psychology',
                'gpaLow' : 3.7,
                'gpaHigh' : 4,
                'major': 'Cognitive Science',
                'university_id': 3
            },
            {
                'programName': 'Biology',
                'gpaLow' : 3.3,
                'gpaHigh' : 3,
                'major': 'Genetics',
                'university_id': 2
            },
            {
                'programName': 'Electrical Engineering',
                'gpaLow' : 3.6,
                'gpaHigh' : 4,
                'major': 'Power Systems',
                'university_id': 1
            },
            {
                'programName': 'English Literature',
                'gpaLow' : 3.8,
                'gpaHigh' : 3,
                'major': 'American Literature',
                'university_id': 3
            },
            {
                'programName': 'Civil Engineering',
                'gpaLow' : 3.2,
                'gpaHigh' : 4,
                'major': 'Structural Engineering',
                'university_id': 1
            },
            {
                'programName': 'Physics',
                'gpaLow' : 3.2,
                'gpaHigh' : 3.9,
                'major': 'Quantum Mechanics',
                'university_id': 2
            },
            {
                'programName': 'Fine Arts',
                'gpaLow' : 3.4,
                'gpaHigh' : 4,
                'major': 'Painting',
                'university_id': 3
            },
            {
                'programName': 'Computer Science',
                'gpaLow' : 3.5,
                'gpaHigh' : 4,
                'major': 'Software Engineering',
                'university_id': 4
            },
            {
                'programName': 'Business Administration',
                'gpaLow' : 3,
                'gpaHigh' : 3.2,
                'major': 'Marketing',
                'university_id': 3
            },
            {
                'programName': 'Mechanical Engineering',
                'gpaLow' : 3.0,
                'gpaHigh' : 4,
                'major': 'Robotics',
                'university_id': 5
            },
            {
                'programName': 'Psychology',
                'gpaLow' : 3.7,
                'gpaHigh' : 4,
                'major': 'Cognitive Science',
                'university_id': 6
            },
            {
                'programName': 'Biology',
                'gpaLow' : 3,
                'gpaHigh' : 3.3,
                'major': 'Genetics',
                'university_id': 1
            },
            {
                'programName': 'Electrical Engineering',
                'gpaLow' : 3.6,
                'gpaHigh' : 4,
                'major': 'Power Systems',
                'university_id': 3
            },
            {
                'programName': 'English Literature',
                'gpaLow' : 3,
                'gpaHigh' : 3.8,
                'major': 'American Literature',
                'university_id': 2
            },
            {
                'programName': 'Civil Engineering',
                'gpaLow' : 3.2,
                'gpaHigh' : 4,
                'major': 'Structural Engineering',
                'university_id': 5
            },
            {
                'programName': 'Physics',
                'gpaLow' : 3,
                'gpaHigh' : 3.9,
                'major': 'Quantum Mechanics',
                'university_id': 2
            },
            {
                'programName': 'Fine Arts',
                'gpaLow' : 3.4,
                'gpaHigh' : 4,
                'major': 'Painting',
                'university_id': 1
            }
        ]

        for data in program_data:
            program = Program(
                programName=data['programName'],
                gpaHigh=data['gpaHigh'],
                gpaLow=data['gpaLow'],
                major=data['major']
            )
            program.university = University.query.get(data['university_id'])
            db.session.add(program)
    return "Success add program"