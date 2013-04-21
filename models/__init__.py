from datetime import datetime, date

from flask.ext.sqlalchemy import SQLAlchemy, sqlalchemy

IntegrityError = sqlalchemy.exc.IntegrityError
desc = sqlalchemy.desc

db = SQLAlchemy()

def get_today():
    t = date.today()
    return datetime(t.year, t.month, t.day)

def init_db(app):
    db.init_app(app)
    db.app = app
    db.create_all()

