from flask import jsonify
from models import models
from controllers import base_controller
import time, datetime
from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash


def create(params, body): 
    #Initialize
    response = {}
    requiredFields = ["recipe_id"]
    optionalFields = []
    allFields = requiredFields + optionalFields
    nutritionFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        nutritionFields[field] = params.get(field, None)
        
    #Check for Optional Fields
    for field in optionalFields:
        if field == "frequency":
            nutritionFields[field] = params.get(field, 0)
        else:
            nutritionFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400

    
    else:
        #Add Nutrition to Database
        nutrition = models.Nutrition(
            recipe_id=nutritionFields["recipe_id"],
            details=body.decode()
        )
        try:
            models.db.session.add(nutrition)
            models.db.session.commit()
            response["message"] = "Nutrition submitted successfully!"
            response["nutrition_id"] = nutrition.nutrition_id
            status = 200
        except:
            response["message"] = "Nutrition couldn't be submitted."
            status = 400
  
    return jsonify(response), status


def show(params):
    #Initialize
    response = {}
    requiredFields = ["nutrition_id"]
    optionalFields = []
    allFields = requiredFields + optionalFields
    nutritionFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        nutritionFields[field] = params.get(field, None)
        
    #Check for Optional Fields
    for field in optionalFields:
        nutritionFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Query for Nutrition
        nutrition = models.Nutrition.query.filter_by(nutrition_id=nutritionFields["nutrition_id"]).first()
        
        if nutrition is not None:
            #Query Successful
            response["nutrition_id"] = nutrition.nutrition_id
            response["recipe_id"] = nutrition.recipe_id
            response["details"] = nutrition.details
            response["message"] = "Nutrition found"
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "Nutrition cannot be found"
            status = 200

    return jsonify(response), status


def display_all(params):
    nutritions = models.Nutrition.query.all()
    response = {}
    for nutrition in nutritions:
        response[nutrition.nutrition_id] = {
            "recipe_id": nutrition.recipe_id,
            "details": nutrition.details
        }
    status = 200
    return jsonify(response), status

def update(params, body):
    #Initialize
    response = {}
    requiredFields = ["nutrition_id"]
    optionalFields = []
    allFields = requiredFields + optionalFields
    nutritionFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        nutritionFields[field] = params.get(field, None)

    #Check for Optional Fields
        for field in optionalFields:
            nutritionFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Query for Nutrition
        nutrition = models.Nutrition.query.filter_by(nutrition_id=nutritionFields["nutrition_id"]).first()     

        if nutrition is not None:
            ''''#Check for Numerical Price and Frequency
            try:
                applFields["user_id"] = int(applFields["user_id"])
            except:
                response["message"] = "Request has incorrect parameter type"
                status = 400
                return jsonify(response), status'''

            #Update nutrition
            nutrition.details = body.decode()
            models.db.session.commit()
            
            #Query Successful
            response["message"] = "Nutrition successfully updated"
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "Nutrition cannot be found"
            status = 200

    return jsonify(response), status

def delete(params):
    #Initialize
    response = {}
    requiredFields = ["nutrition_id"]
    optionalFields = []
    allFields = requiredFields + optionalFields
    nutritionFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        nutritionFields[field] = params.get(field, None)
        
    #Check for Optional Fields
    for field in optionalFields:
        nutritionFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Query for Nutrition
        nutrition = models.Nutrition.query.filter_by(nutrition_id=nutritionFields["nutrition_id"]).first()
        
        if nutrition is not None:
            #Query Successful
            models.db.session.delete(nutrition)
            models.db.session.commit()
            response["message"] = "Nutrition successfully removed"
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "Nutrition cannot be found"
            status = 200

    return jsonify(response), status