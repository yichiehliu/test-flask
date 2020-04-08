import time
from datetime import timedelta
import json
from sqlalchemy import and_, func
import os
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask import request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, jsonify
from flask import Flask
from config import Config

from flask import Blueprint
main = Blueprint('main', __name__)

#  取得啟動文件資料夾路徑
pjdir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object(Config)
#  新版本的部份預設為none，會有異常，再設置True即可。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#  設置資料庫為sqlite3
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                        os.path.join(
                                            pjdir, 'data0320_12.sqlite')
app.config['SECRET_KEY'] = '\xf0?a\x9a\\\xff\xd4;\x0c\xcbHi'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


def create_app():
    app = Flask(__name__)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint) // 註冊藍本

    return app
