from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_bootstrap import Bootstrap
import click


bootstrap = Bootstrap()
db = SQLAlchemy()
csrf = CSRFProtect()
moment = Moment()
toolbar = DebugToolbarExtension()
migrate = Migrate()
