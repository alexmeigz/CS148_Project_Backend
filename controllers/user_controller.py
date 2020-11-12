from flask import jsonify
from models import models
from controllers import base_controller
import time, datetime
from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash


def create(params): 
    #Initialize
    response = {}
    requiredFields = ["username", "email", "account_type", "password_hash"]
    optionalFields = ["vendor_location"]
    allFields = requiredFields + optionalFields
    userFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        userFields[field] = params.get(field, None)
        
    #Check for Optional Fields
    for field in optionalFields:
        if field == "frequency":
            userFields[field] = params.get(field, 0)
        else:
            userFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Add User to Database
        user = models.User(
            username=userFields["username"],
            email=userFields["email"],
            account_type=userFields["account_type"],
            password_hash = userFields["password_hash"],
            vendor_location=userFields["vendor_location"],
            credits=0
            )
        try:
            models.db.session.add(user)
            models.db.session.commit()
            response["message"] = "User created successfully!"
            status = 200
        except:
            response["message"] = "Username already exists."
            status = 400
  
    return jsonify(response), status


def login(params):
    #Initialize
    response = {}
    requiredFields = ["username", "login", "password_hash"]
    optionalFields = []
    allFields = requiredFields + optionalFields
    userFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        userFields[field] = params.get(field, None)
        
    #Check for Optional Fields
    for field in optionalFields:
        userFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Query for User
        user = models.User.query.filter_by(username=userFields["username"]).first()
        if(not user):
            response["message"] = "Invalid username"
            status = 400
            return jsonify(response), status
        elif(user.password_hash != userFields["password_hash"]):
            response["message"] = "Invalid password"
            status = 400
            return jsonify(response), status

        if user is not None:
            #Query Successful
            response["user_id"] = user.user_id
            response["username"] = user.username
            response["email"] = user.email
            response["account_type"] = user.account_type
            response["vendor_location"] = user.vendor_location
            response["credits"] = user.credits
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "User cannot be found"
            status = 400

    return jsonify(response), status

def show(params):
    #Initialize
    response = {}
    requiredFields = ["user_id"]
    optionalFields = []
    allFields = requiredFields + optionalFields
    userFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        userFields[field] = params.get(field, None)
        
    #Check for Optional Fields
    for field in optionalFields:
        userFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Query for User
        user = models.User.query.filter_by(user_id=userFields["user_id"]).first()

        if user is not None:
            #Query Successful
            response["user_id"] = user.user_id
            response["username"] = user.username
            response["email"] = user.email
            response["account_type"] = user.account_type
            response["vendor_location"] = user.vendor_location
            response["credits"] = user.credits
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "User cannot be found"
            status = 400

    return jsonify(response), status

def update(params):
    #Initialize
    response = {}
    requiredFields = ["user_id", "username", "email", "account_type", "credits"]
    optionalFields = ["vendor_location"]
    allFields = requiredFields + optionalFields
    userFields = {}
    print(params)
    print(requiredFields)

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        userFields[field] = params.get(field, None)

    #Check for Optional Fields
        for field in optionalFields:
            userFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Query for User
        user = models.User.query.filter_by(user_id=userFields["user_id"]).first()     

        if user is not None:
            #Check for Numerical Credits
            try:
                userFields["credits"] = float(userFields["credits"])
            except:
                response["message"] = "Request has incorrect parameter type"
                status = 400
                return jsonify(response), status

            #Update User
            user.credits = userFields["credits"]
            user.email = userFields["email"]
            user.account_type = userFields["account_type"]
            user.vendor_location = userFields["vendor_location"]
            models.db.session.commit()
            
            #Query Successful
            response["message"] = "User successfully updated"
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "User cannot be found"
            status = 400

    return jsonify(response), status

def delete(params):
    #Initialize
    response = {}
    requiredFields = ["user_id"]
    optionalFields = []
    allFields = requiredFields + optionalFields
    userFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        userFields[field] = params.get(field, None)
        
    #Check for Optional Fields
    for field in optionalFields:
        userFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Query for User
        user = models.User.query.filter_by(user_id=userFields["user_id"]).first()
        
        if user is not None:
            #Query Successful
            models.db.session.delete(user)
            models.db.session.commit()
            response["message"] = "User successfully removed"
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "User cannot be found"
            status = 400

    return jsonify(response), status