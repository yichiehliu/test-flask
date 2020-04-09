from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user

from app.api import LoginForm
from bluelog.models import Admin
from bluelog.utils import redirect_back
