from models import *
import datetime

class Product(BaseModel, db.Model):
    """Model for the stations table"""
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    subscription = db.Column(db.Boolean)
    frequency = db.Column(db.Interval)
    price = db.Column(db.Float)
    list_date = db.Column(db.Date)
    location = db.Column(db.Text)
    nutrition_id = db.Column(db.Integer)


