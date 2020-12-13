from flask import jsonify
from models import models
from controllers import base_controller
import time, datetime
from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

def create(params): 
    #Initialize
    response = {}
    requiredFields = ["recipe_id"]
    optionalFields = ["calories", "fat", "saturated", "trans", "carbs", "fiber", "sugars", "protein", "cholesterol", "sodium"]
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
        if params.get(field, None):
            nutritionFields[field] = round(float(params.get(field)),2)
        else:
            nutritionFields[field] = "Unknown"
            
    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400

    
    else:
        #Add Nutrition to Database
        nutrition = models.Nutrition(
            recipe_id=nutritionFields["recipe_id"],
            calories = str(nutritionFields["calories"]) + " cal",
            fat = str(nutritionFields["fat"]) + " g",
            saturated = str(nutritionFields["saturated"]) + " g",
            trans = str(nutritionFields["trans"]) + " g",
            carbs = str(nutritionFields["carbs"]) + " g",
            fiber = str(nutritionFields["fiber"]) + " g",
            sugars = str(nutritionFields["sugars"]) + " g",
            protein = str(nutritionFields["protein"]) + " g",
            cholesterol = str(nutritionFields["cholesterol"]) + " mg",
            sodium = str(nutritionFields["sodium"]) + " mg"
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
            response["calories"] = nutrition.calories
            response["fat"] = nutrition.fat
            response["saturated"] = nutrition.saturated
            response["trans"] = nutrition.trans
            response["carbs"] = nutrition.carbs
            response["fiber"] = nutrition.fiber
            response["sugars"] = nutrition.sugars
            response["protein"] = nutrition.protein
            response["cholesterol"] = nutrition.cholesterol
            response["sodium"] = nutrition.sodium
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
            "calories": nutrition.calories,
            "fat": nutrition.fat,
            "saturated": nutrition.saturated,
            "trans": nutrition.trans,
            "carbs": nutrition.carbs,
            "fiber": nutrition.fiber,
            "sugars": nutrition.sugars,
            "protein": nutrition.protein,
            "cholesterol": nutrition.cholesterol,
            "sodium": nutrition.sodium
        }
    status = 200
    return jsonify(response), status

def update(params):
    #Initialize
    response = {}
    requiredFields = ["nutrition_id"]
    optionalFields = ["calories", "fat", "saturated", "trans", "carbs", "fiber", "sugars", "protein", "cholesterol", "sodium"]
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
            #Update nutrition
            if(params.get("calories", None)):
                nutrition.calories = str(nutritionFields["calories"]) + " cal"

            if(params.get("fat", None)):
                nutrition.fat = str(nutritionFields["fat"]) + " g"

            if(params.get("saturated", None)):
                nutrition.saturated= str(nutritionFields["saturated"]) + " g"

            if(params.get("trans", None)):
                nutrition.trans = str(nutritionFields["trans"]) + " g"

            if(params.get("carbs", None)):
                nutrition.carbs = str(nutritionFields["carbs"]) + " g"

            if(params.get("fiber", None)):
                nutrition.fiber = str(nutritionFields["fiber"]) + " g"

            if(params.get("sugars", None)):
                nutrition.sugars = str(nutritionFields["sugars"]) + " g"

            if(params.get("protein", None)):
                nutrition.protein = str(nutritionFields["protein"]) + " g"

            if(params.get("cholesterol", None)):
                nutrition.cholesterol = str(nutritionFields["cholesterol"]) + " mg"

            if(params.get("sodium", None)):
                nutrition.sodium = str(nutritionFields["sodium"]) + " mg"

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
        nutritionFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Query for Nutrition
        nutrition = models.Nutrition.query.filter_by(recipe_id=nutritionFields["recipe_id"]).first()
        
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