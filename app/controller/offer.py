#controller
from flask import Blueprint, render_template, request
from app.models.base import db
from app.models.offer import Offer
from app.models.offer_tac import Offer_tac
from app.models.offer_com import Offer_com
from app.models.offer_res import Offer_res
from app.models.program import Program

import random
offerBP = Blueprint('offer', __name__)

@offerBP.route('/', methods=['GET'])
def offer():
    return render_template('offer.html')

@offerBP.route('/add', methods=['GET'])
def add_offer():
    if request.method == 'GET':
        return render_template('add_offer.html')

@offerBP.route('/view',methods=['GET'])
def view_offer():
    if request.method=='GET':
        return render_template('view_offer.html')

@offerBP.route('/auto_add',methods=['GET'])
def auto_add():
    with db.auto_commit():
        programs = Program.query.all()  # 获取所有程序对象
        program_ids = [program.id for program in programs]  # 提取程序对象的ID列表

        for _ in range(5):
            gpa = round(random.uniform(2.5, 4), 2)  # 生成在2.5和4之间的随机数，并保留两位小数
            offer_tac = Offer_tac("2021/10/12", gpa, None)
            program_id = random.choice(program_ids)  # 从程序ID列表中随机选择一个ID
            offer_tac.program = Program.query.get(program_id)  # 获取对应的程序对象
            db.session.add(offer_tac)  # 添加到会话中

        for _ in range(5):
            gpa = round(random.uniform(2.5, 4), 2)  # 生成在2.5和4之间的随机数，并保留两位小数
            offer_tac = Offer_tac("2022/10/12", gpa, None)
            program_id = random.choice(program_ids)  # 从程序ID列表中随机选择一个ID
            offer_tac.program = Program.query.get(program_id)  # 获取对应的程序对象
            db.session.add(offer_tac)  # 添加到会话中

    with db.auto_commit():
        programs = Program.query.all()  # 获取所有程序对象
        program_ids = [program.id for program in programs]  # 提取程序对象的ID列表

        for _ in range(5):
            gpa = round(random.uniform(2.5, 4), 2)  # 生成在2.5和4之间的随机数，并保留两位小数
            offer_res = Offer_res("2021/10/12", gpa, None, None, None, None, None, None)
            program_id = random.choice(program_ids)  # 从程序ID列表中随机选择一个ID
            offer_res.program = Program.query.get(program_id)  # 获取对应的程序对象
            db.session.add(offer_res)  # 添加到会话中

        for _ in range(5):
            gpa = round(random.uniform(2.5, 4), 2)  # 生成在2.5和4之间的随机数，并保留两位小数
            offer_res = Offer_res("2020/10/12", gpa, None, None, None, None, None, None)
            program_id = random.choice(program_ids)  # 从程序ID列表中随机选择一个ID
            offer_res.program = Program.query.get(program_id)  # 获取对应的程序对象
            db.session.add(offer_res)  # 添加到会话中

    with db.auto_commit():
        programs = Program.query.all()  # 获取所有程序对象

        for _ in range(5):
            gpa = round(random.uniform(2.5, 4), 2)  # 生成在2.5和4之间的随机数，并保留两位小数
            offer_com = Offer_com("2019/10/12", gpa, None, 'name', 'name', None)

            db.session.add(offer_com)  # 添加到会话中

        for _ in range(5):
            gpa = round(random.uniform(2.5, 4), 2)  # 生成在2.5和4之间的随机数，并保留两位小数
            offer_com = Offer_com("2020/10/12", gpa, None, 'name', 'name', None)

            db.session.add(offer_com)  # 添加到会话中

    return "offer add successfully"