import os
from flask import Flask
from RealProject.settings import BASE_DIR
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
 # 操作数据库
db = SQLAlchemy()
migeate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

   

    if test_config is None:
        CONFIG_PATH = BASE_DIR / 'RealProject/settings.py'
        app.config.from_pyfile(CONFIG_PATH,silent=True)
    else:
        # 最开始的配置一致意思
        app.config_mapping(test_config)

    db.init_app(app) 
    migeate.init_app(app, db)

    # 引入blog的视图文件      
    from app.blog import views as blog
    app.register_blueprint(blog.bp)
    from app.auth import views as auth
    app.register_blueprint(auth.bp)
    #URL引入
    app.add_url_rule('/', endpoint='index', view_func=blog.index)

    # 注册数据库模型
    from app.blog import models
    from app.auth import models
    return app
