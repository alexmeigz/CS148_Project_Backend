from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin #for user login
from werkzeug.security import generate_password_hash, check_password_hash # for pwd hashing

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


class User(UserMixin, db.Model):
    """Model for the users"""
    
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.Text)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.Text)
    account_type = db.Column(db.Text)
    vendor_location = db.Column(db.Text, nullable = True)
    #vendor_product_list = db.Column(ARRAY(db.Text)) #https://groups.google.com/g/sqlalchemy/c/5aTmT4rUJo4?pli=1
    #credits = db.Column(db.Integer)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)