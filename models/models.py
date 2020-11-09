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
    caption = db.Column(db.Text)
    subscription = db.Column(db.Boolean)
    frequency = db.Column(db.Interval)
    price = db.Column(db.Float)
    list_date = db.Column(db.Date)
    location = db.Column(db.Text)
    nutrition_id = db.Column(db.Integer)

class Post(db.Model):
    """Model for the stations table"""
    
    __tablename__ = 'post'

    post_id = db.Column(db.Integer, primary_key = True)
    post_type = db.Column(db.Text)          #one of ["blog", "recipe", "review"]
    title = db.Column(db.Text)
    content = db.Column(db.Text)            #only for blog/review (in binary)
    rating = db.Column(db.Float)            #only for review
    caption = db.Column(db.Text)            #only for recipe
    ingredients = db.Column(db.Text)        #only for recipe
    instructions = db.Column(db.Text)       #only for recipe
    last_edit = db.Column(db.DateTime)

