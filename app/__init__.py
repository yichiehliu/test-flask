import click
import time
from datetime import timedelta
import json
import os

from app.config import Config
from app.extensions import db, csrf, moment, toolbar, migrate
# from app.models import ReservedCarStatus, resrvRecord, CarAllinfo, QueryRecord, OrderRecord
from app.models import realtime_models, reserve_models

from flask_sqlalchemy import SQLAlchemy, get_debug_queries
from flask import Flask, render_template, request, jsonify
from sqlalchemy import and_, func
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from app.blueprints.car import car_bp
from app.blueprints.realtime import realtime_bp
from app.blueprints.reservation import resrv_bp


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('CONFIG', 'development')

    app = Flask(__name__)  # 名字是要怎麼取? 自己隨便取? 資料夾的名稱?
    app.config.from_object(Config)
    # 原本都寫在create_app裡面，但太多了，所以拆成不同的register(configurate)函是
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    # register_shell_context(app)
    # register_template_context(app)
    # register_request_handlers(app)
    return app


def register_extensions(app):
    # bootstrap.init_app(app)
    db.init_app(app)
    csrf.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(car_bp)
    app.register_blueprint(realtime_bp, url_prefix='/api/realtime')
    app.register_blueprint(resrv_bp, url_prefix='/api/resrvmode')
    
def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return 400

    @app.errorhandler(404)
    def page_not_found(e):
        return 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return 500



def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

        db.session.commit()
        click.echo('Done.')

    @app.cli.command()
    @click.option('--car', default=10, help='Quantity of cars, default is 10.')
    @click.option('--rentables', default=10, help='Quantity of rentalable cars, default is 10.')
    @click.option('--query', default=50, help='Quantity of queries, default is 10.')
    @click.option('--order', default=50, help='Quantity of orders, default is 10.')
    def forge(car, rentables, query, order):
        """Generate fake data."""
        from app.fakes import fake_car, fake_query, fake_orders

        db.drop_all()
        db.create_all()

        click.echo('Generating the cars...')
        fake_car()

        # click.echo('Generating %d categories...' % category)
        # fake_categories(category)

        # click.echo('Generating %d posts...' % post)
        # fake_posts(post)

        # click.echo('Generating %d comments...' % comment)
        # fake_comments(comment)

        # click.echo('Generating links...')
        # fake_links()

        click.echo('Done.')