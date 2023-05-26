from flask import Flask
# import sys
# sys.path.append('C:/Users/23689/Desktop/project_v1')

# from app.controller import book, student, teacher, user, program, offer, offer_tau
from app.controller import program,university,uicer,alumni,offer, report, knowledge_point,offer_com, offer_tac,offer_res,gpt

# 定义注册蓝图方法
def register_blueprints(app):
    app.register_blueprint(program.programBP, url_prefix='/program')
    app.register_blueprint(university.universityBP, url_prefix='/university')
    app.register_blueprint(uicer.uicerBP, url_prefix='/uicer')
    app.register_blueprint(alumni.alumniBP, url_prefix='/alumni')
    app.register_blueprint(offer.offerBP, url_prefix='/offer')
    app.register_blueprint(offer_com.offer_comBP, url_prefix='/offer_com')
    app.register_blueprint(offer_tac.offer_tacBP, url_prefix='/offer_tac')
    app.register_blueprint(offer_res.offer_resBP, url_prefix='/offer_res')
    app.register_blueprint(report.reportBP, url_prefix='/report')
    app.register_blueprint(knowledge_point.kpBP, url_prefix='/kp')
    app.register_blueprint(gpt.gptBP, url_prefix='/gpt')
    # app.register_blueprint(offer.offerBP, url_prefix='/offer')
    # app.register_blueprint(offer_tau.offer_tauBP, url_prefix='/offer_tau')


# 注册插件(数据库关联)
def register_plugin(app):
    from app.models.base import db
    db.init_app(app)
    # create_all要放到app上下文环境中使用
    with app.app_context():
        db.create_all()


def create_app():
    app = Flask(__name__)
    # app.config.from_object('app.config.setting') # 基本配置(setting.py)
    app.config.from_object('app.config.secure')  # 重要参数配置(secure.py)
    # 注册蓝图与app对象相关联
    register_blueprints(app)
    # 注册插件(数据库)与app对象相关联
    register_plugin(app)
    # 一定要记得返回app
    return app
