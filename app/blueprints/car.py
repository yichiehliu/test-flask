from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import request, Blueprint
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import os
from sqlalchemy import and_, func
import json
from datetime import timedelta
import time
from app.models import CarAllinfo, FONLoc, RealtimeCarDetails, RealtimeCarOrderRecord, ReservedCarStatus, QueryRecord, BookingRecord, OrderRecord


car_bp = Blueprint('car', __name__)
