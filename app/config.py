
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask import request
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import os
from sqlalchemy import and_, func
import json
from datetime import timedelta
import time


class Config:
    pjdir = os.path.abspath(os.path.dirname(__file__))
    DEBUG = True
    PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(pjdir, 'data.sqlite')
    SECRET_KEY = b'\xb9k\xdf@\x0e\x1f(\xf2\xb0\xd0\xcb?Y\xdcN\x19G\x12e\xa8\x8b\xe5\xccS'
