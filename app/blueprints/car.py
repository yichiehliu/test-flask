from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user


from app.models import CarStatus, OrderRecord, CarModelRelation, QueryRecord
from bluelog.utils import redirect_back

car_bp = Blueprint('car', 'rentlog')
