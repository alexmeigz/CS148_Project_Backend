from flask import jsonify
from models import models
from controllers import base_controller, post_controller, appl_controller, product_controller, report_controller
import time, datetime
from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash


def create(params): 
    #Initialize
    response = {}
    requiredFields = ["username", "email", "password_hash"]
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
            account_type="Normal",
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
        elif(user.password_hash != userFields["password_hash"].strip()):
            response["message"] = "Invalid password"
            status = 400
            return jsonify(response), status

        if user is not None:
            #Query Successful
            response["user_id"] = user.user_id
            response["username"] = user.username
            response["email"] = user.email
            response["instagram"] = user.instagram
            response["account_type"] = user.account_type
            response["vendor_location"] = user.vendor_location
            response["credits"] = user.credits
            response["profile_image_url"] = user.profile_image_url
            response["vendor_image_url"] = user.vendor_image_url
            response["vendor_name"] = user.vendor_name
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
            response["instagram"] = user.instagram
            response["account_type"] = user.account_type
            response["vendor_location"] = user.vendor_location
            response["vendor_name"] = user.vendor_name
            response["credits"] = user.credits
            response["profile_image_url"] = user.profile_image_url
            response["vendor_image_url"] = user.vendor_image_url
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "User cannot be found"
            status = 400

    return jsonify(response), status

def display_all(params):
    q = models.User.query
    if(params.get("vendor_name", None != None)):
        q = q.filter(models.User.vendor_name.contains(params["vendor_name"]))

    if params.get("filter", None) == "vendor":
        users = (q.filter_by(account_type="Business").all() + 
                    q.filter_by(account_type="Home").all())
    else:
        users = q.all()
    
    response = {}
    for user in users:
        response[user.user_id] = {
            "user_id" : user.user_id,
            "username" : user.username,
            "email" : user.email,
            "instagram" : user.instagram,
            "account_type" : user.account_type,
            "vendor_location" : user.vendor_location,
            "vendor_name" : user.vendor_name,
            "credits" : user.credits,
            "profile_image_url" : user.profile_image_url,
            "vendor_image_url" : user.vendor_image_url
        }
    status = 200

    return jsonify(response), status

def update(params):
    #Initialize
    response = {}
    requiredFields = ["user_id"]
    optionalFields = ["vendor_location", "vendor_name", "email", "account_type", "credits", "vendor_image_url", "profile_image_url", "instagram"]
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
            #Update User
            if(userFields.get("credits", None)):
                #Check for Numerical Credits
                try:
                    userFields["credits"] = float(userFields["credits"])
                except:
                    response["message"] = "Request has incorrect parameter type"
                    status = 400
                    return jsonify(response), status
                user.credits = userFields["credits"]

            if(userFields.get("vendor_name", None)):
                user.vendor_name = userFields["vendor_name"]
            if(userFields.get("email", None)):
                user.email = userFields["email"]
            if(userFields.get("instagram", None)):
                user.instagram = userFields["instagram"]
            if(userFields.get("account_type", None)):
                user.account_type = userFields["account_type"]
            if(userFields.get("vendor_location", None)):
                user.vendor_location = userFields["vendor_location"]
            if(userFields.get("profile_image_url", None)):
                user.profile_image_url = userFields["profile_image_url"]
            if(userFields.get("vendor_image_url", None)):
                user.vendor_image_url = userFields["vendor_image_url"]
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

            try:
                post_controller.delete_all({"user_id" : user.user_id})
            except:
                response["message"] = "Error removing posts."
                status = 400   
                return jsonify(response), status 
            
            try:
                appl_controller.delete_all({"user_id" : user.user_id})
            except:
                response["message"] = "Error removing vendor apps."
                status = 400   
                return jsonify(response), status 
            
            try:
                message, product_status = product_controller.delete_all({"vendor_id" : user.user_id})
                print(message, product_status)
            except:
                response["message"] = "Error removing products."
                status = 400   
                return jsonify(response), status

            try:
                report_controller.delete_all({"userReporter_id" : user.user_id})
            except:
                response["message"] = "Error removing reports."
                status = 400   
                return jsonify(response), status




            models.db.session.delete(user)
            models.db.session.commit()
            response["message"] = "User successfully removed"
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "User cannot be found"
            status = 400

    return jsonify(response), status

