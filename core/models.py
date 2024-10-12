from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.Text)
    description = db.Column(db.Text)


class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.Text)
    account_balance = db.Column(db.Numeric)


def row_to_dict(row):
    return {column.name: getattr(row, column.name) for column in row.__table__.columns}
