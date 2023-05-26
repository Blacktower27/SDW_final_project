from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import func
from app.models.base import db
from app.models.alumni import Alumni
from app.controller.forms import RegistForm
import openai
import json

gptBP = Blueprint('gptBP',__name__)

openai.api_key = 'your openai API'

@gptBP.route('advice', methods=['GET','POST'])
def advice():
    if request.method=='GET':
        return render_template('advice.html')
    else:
        q1=request.form.get('q1')
        q2 = request.form.get('q2')
        q3 = request.form.get('q3')
        q4 = request.form.get('q4')
        question = 'Let us say I am an undergraduate student applying to a graduate program. Here is some of my personal information. My undergraduate major is: '+q1+', I hope to study as: '+q2+'graduate student, my career goal and my interests are: '+q3+', and I hope to study as a graduate student in: '+q4+'. Please recommend 15 graduate programs to me.please reply as json named:programs include university_name, program_name and reason.'
        messages = [{"role": "system", "content": question}]
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
        reply = chat.choices[0].message.content
        # print(reply)
        data = json.loads(reply)
        print(data)
        programs = data['programs']
        # for program in programs:
        #     print(program['university_name'])
        #     print(program['program_name'])
        #     print(program['reason'])
        #     print('---------------------------')
        return render_template('advice.html',programs=programs)

