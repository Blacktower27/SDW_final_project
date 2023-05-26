## import libraries
from app import create_app
import flask
from app.models.uicer import Uicer
from app.models.alumni import Alumni
# from flask_wtf.csrf import CSRFProtect
# from flask_uploads import UploadSet, configure_uploads, IMAGES




app = create_app()
#初始化上传图片的扩展
# 初始化CSRF保护
# csrf = CSRFProtect(app)
#
# # 初始化上传集合和配置
# photos = UploadSet('photos', IMAGES)
# configure_uploads(app, photos)

@app.before_request
def before_request():
    id = flask.session.get('id')
    alumni = Alumni.query.get(id)
    uicer = Uicer.query.get(id)
    if alumni:
        setattr(flask.g,'uicer',None)
        setattr(flask.g, 'alumni', alumni)
    elif uicer:
        setattr(flask.g, 'uicer', uicer)
        setattr(flask.g, 'alumni', None)
    else:
        setattr(flask.g, 'uicer', None)
        setattr(flask.g, 'alumni', None)

@app.context_processor
def context_processor():
    return {"uicer":flask.g.uicer,"alumni":flask.g.alumni}

if __name__ == '__main__':
    # 启动应用服务器, 使用默认参数, 开启调试模式
    app.run(debug=True,host='127.0.0.1', port=5000)    
    # app.run(host='0.0.0.0', port=5001)


