from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
#Base Code Acquired from https://blog.theodo.com/2017/03/developping-a-flask-web-app-with-a-postresql-database-making-all-the-possible-errors/
class BaseModel(db.Model):
    '''Base data model for all objects'''
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        '''Define a base way to print models'''
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        '''Define a base way to jsonify models, dealing with datetime objects''' 
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }

class Product(db.Model):
    """Model for the stations table"""
    
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key = True)
    vendor_id = db.Column(db.Integer)
    name = db.Column(db.Text)
    subscription = db.Column(db.Boolean)
    frequency = db.Column(db.Interval)
    price = db.Column(db.Float)
    list_date = db.Column(db.Date)
    location = db.Column(db.Text)
    nutrition_id = db.Column(db.Integer)

class Application(db.Model):
    """Model for the stations table"""
    
    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    restName = db.Column(db.Text)
    vendorType = db.Column(db.Text)
    applsDate = db.Column(db.Date)
    busLocation = db.Column(db.Text)
    reason = db.Column(db.Text)