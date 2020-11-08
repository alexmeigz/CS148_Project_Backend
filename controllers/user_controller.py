from flask import jsonify
from models import models
from controllers import base_controller
import time, datetime


def create(params): 
    #Initialize
    response = {}
    requiredFields = ["username", "email", "account_type"]
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
        ''' Don't need to account for numerical data as of now
        #Check for Numerical Price and Frequency
        try:
            productFields["price"] = float(productFields["price"])
            productFields["vendor_id"] = int(productFields["vendor_id"])
            productFields["frequency"] = int(productFields["frequency"])
        except:
            response["message"] = "Request has incorrect parameter type"
            status = 400
            return jsonify(response), status
        '''
        #Add User to Database
        user = models.User(
            username=userFields["username"],
            email=userFields["email"],
            account_type=userFields["account_type"],
            vendor_location=userFields["vendor_location"],
            )
        models.db.session.add(user)
        models.db.session.commit()
        response["message"] = "User created successfully!"
        status = 200
  
    return jsonify(response), status


def show(params):
    #Initialize
    response = {}
    requiredFields = ["id"]
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
        user = models.User.query.filter_by(id=userFields["id"]).first()
        
        if user is not None:
            #Query Successful
            response["user_id"] = user.user_id
            response["username"] = user.username
            response["email"] = user.email
            response["account_type"] = user.account_type
            response["vendor_location"] = user.vendor_location
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "Product cannot be found"
            status = 200

    return jsonify(response), status

def update(params):
    #Initialize
    response = {}
    requiredFields = ["username", "email", "account_type"]
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
            userFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Query for User
        user = models.User.query.filter_by(id=userFields["id"]).first()     

        if user is not None:
            ''' Wont need to update any numerical values
            #Check for Numerical Price and Frequency
            try:
                productFields["price"] = float(productFields["price"])
                productFields["frequency"] = int(productFields["frequency"])
            except:
                response["message"] = "Request has incorrect parameter type"
                status = 400
                return jsonify(response), status
'''
            #Update User
            user.name = userFields["username"]
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
            status = 200

    return jsonify(response), status

def delete(params):
    #Initialize
    response = {}
    requiredFields = ["id"]
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
        user = models.User.query.filter_by(id=userFields["id"]).first()
        
        if user is not None:
            #Query Successful
            models.db.session.delete(user)
            models.db.session.commit()
            response["message"] = "User successfully removed"
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "User cannot be found"
            status = 200

    return jsonify(response), status