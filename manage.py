from app import app
from app import create_app
import click
from flask_click_migrate import Migrate, MigrateGroup
from models import db
from main import app


migrate = Migrate(app, db)

# db.create_all()


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
