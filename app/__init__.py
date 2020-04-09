from app.config import Config
from app.extensions import bootstrap, db, login_manager, csrf, ckeditor, mail, moment, toolbar, migrate
from app.models import CarStatus, OrderRecord, CarModelRelation, QueryRecord
from flask_wtf.csrf import CSRFError
from flask_sqlalchemy import get_debug_queries
from flask_login import current_user
from flask import Flask, render_template, request
import click
from logging.handlers import SMTPHandler, RotatingFileHandler
import logging
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

from app.blueprints.car import car_bp
from app.blueprints.order import order_bp
from app.blueprints.query import query_bp

from app.extensions import bootstrap, db, login_manager, csrf, ckeditor, mail, moment, toolbar, migrate


#  取得啟動文件資料夾路徑
basedir = os.path.abspath(os.path.dirname(__file__))

# app = Flask(__name__)
# app.config.from_object(Config)
#  新版本的部份預設為none，會有異常，再設置True即可。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#  設置資料庫為sqlite3
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                        os.path.join(
                                            pjdir, 'data0320_12.sqlite')
app.config['SECRET_KEY'] = '\xf0?a\x9a\\\xff\xd4;\x0c\xcbHi'


def create_app(config_name=Config):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('rent')  # 名字是要怎麼取? 自己隨便取? 資料夾的名稱?
    app.config.from_object(config[config_name])
    # 原本都寫在create_app裡面，但太多了，所以拆成不同的register(configurate)函是
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_shell_context(app)
    register_template_context(app)
    register_request_handlers(app)
    return app


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app, db)
