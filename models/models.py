from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin #for user login
from werkzeug.security import generate_password_hash, check_password_hash # for pwd hashing

db = SQLAlchemy()

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
    image_url = db.Column(db.Text)

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
    user_id = db.Column(db.Integer)     
    image_url = db.Column(db.Text)
    last_edit = db.Column(db.DateTime)

class User(db.Model):
    """Model for the users"""
    
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.Text, unique = True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.Text)
    account_type = db.Column(db.Text)
    vendor_location = db.Column(db.Text, nullable = True)
    #vendor_product_list = db.Column(ARRAY(db.Text)) #https://groups.google.com/g/sqlalchemy/c/5aTmT4rUJo4?pli=1
    credits = db.Column(db.Float)
    profile_image_url = db.Column(db.Text)
    vendor_image_url = db.Column(db.Text)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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

class Report(db.Model):
    """Model for the stations table"""
    
    __tablename__ = 'report'

    report_id = db.Column(db.Integer, primary_key = True)
    userReporter_id = db.Column(db.Integer)
    reportedUser_id = db.Column(db.Integer)
    reportText = db.Column(db.Text)
    reportDate = db.Column(db.Date)

class Nutrition(db.Model):
    """Model for the stations table"""
    
    __tablename__ = 'nutrition'

    nutrition_id = db.Column(db.Integer, primary_key = True)
    recipe_id = db.Column(db.Integer)
    details = db.Column(db.Text)

class Reaction(db.Model):
    """Model for the stations table"""
    
    __tablename__ = 'reaction'

    reaction_id = db.Column(db.Integer, primary_key = True)
    post_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

class Comment(db.Model):
    
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key = True)
    post_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    com_date = db.Column(db.Date)
    com_info = db.Column(db.Text)