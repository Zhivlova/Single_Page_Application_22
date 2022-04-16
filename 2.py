from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

application = Flask(__name__)
application.debug = True
application.config['SECRET_KEY'] = 'a really really really really long secret key'
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass@localhost/flask_app_db'

manager = Manager(application)
db = SQLAlchemy(application)


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.BigInteger(), primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    parameters = db.relationship('Parameter', backref='item', uselist=False)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.title[:10])

class Parameter(db.Model):
    __tablename__ = 'parameters'
    item_id = db.Column(db.BigInteger(), db.ForeignKey('item_id'))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    date = db.Column(db.Date())
    quantity = db.Column(db.BigInteger())
    distance = db.Column(db.BigInteger())

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.title[:10])
