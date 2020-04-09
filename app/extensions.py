from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_mail import Mail
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap
from app import app
from app import create_app
import click
from flask_click_migrate import Migrate, MigrateGroup


bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
ckeditor = CKEditor()
mail = Mail()
moment = Moment()
toolbar = DebugToolbarExtension()
migrate = Migrate()
