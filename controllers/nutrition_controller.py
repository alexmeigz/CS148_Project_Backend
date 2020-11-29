from flask import jsonify
from models import models
from controllers import base_controller
import time, datetime
from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash


def create(params): 
    #Initialize
    response = {}
    requiredFields = ["recipe_id", "calories", "fat", "sat_fat", "trans_fat", "carbs", "fiber", "sugar", "protein", "chol", "sodium"]
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
            calories = str(nutritionFields["calories"]) + "cal",
            fat = str(nutritionFields["fat"]) + "g",
            sat_fat = str(nutritionFields["sat_fat"]) + "g",
            trans_fat = str(nutritionFields["trans_fat"]) + "g",
            carbs = str(nutritionFields["carbs"]) + "g",
            fiber = str(nutritionFields["fiber"]) + "g",
            sugar= str(nutritionFields["sugar"]) + "g",
            protein = str(nutritionFields["protein"]) + "g",
            chol = str(nutritionFields["chol"]) + "mg",
            sodium = str(nutritionFields["sodium"]) + "mg"
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
            response["sat_fat"] = nutrition.sat_fat
            response["trans_fat"] = nutrition.trans_fat
            response["carbs"] = nutrition.carbs
            response["fiber"] = nutrition.fiber
            response["sugar"] = nutrition.sugar
            response["protein"] = nutrition.protein
            response["chol"] = nutrition.chol
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
            "sat_fat": nutrition.sat_fat,
            "trans_fat": nutrition.trans_fat,
            "carbs": nutrition.carbs,
            "fiber": nutrition.fiber,
            "sugar": nutrition.sugar,
            "protein": nutrition.protein,
            "chol": nutrition.chol,
            "sodium": nutrition.sodium
        }
    status = 200
    return jsonify(response), status

def update(params):
    #Initialize
    response = {}
    requiredFields = ["nutrition_id"]
    optionalFields = ["calories", "fat", "sat_fat", "trans_fat", "carbs", "fiber", "sugar", "protein", "chol", "sodium"]
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
            if(params.get("calories", None)):
                nutrition.calories = str(nutritionFields["calories"]) + "cal"

            if(params.get("fat", None)):
                nutrition.fat = str(nutritionFields["fat"]) + "g"

            if(params.get("sat_fat", None)):
                nutrition.sat_fat= str(nutritionFields["sat_fat"]) + "g"

            if(params.get("trans_fat", None)):
                nutrition.trans_fat = str(nutritionFields["trans_fat"]) + "g"

            if(params.get("carbs", None)):
                nutrition.carbs = str(nutritionFields["carbs"]) + "g"

            if(params.get("fiber", None)):
                nutrition.fiber = str(nutritionFields["fiber"]) + "g"

            if(params.get("sugar", None)):
                nutrition.sugar = str(nutritionFields["sugar"]) + "g"

            if(params.get("protein", None)):
                nutrition.protein = str(nutritionFields["protein"]) + "g"

            if(params.get("chol", None)):
                nutrition.chol = str(nutritionFields["chol"]) + "mg"

            if(params.get("sodium", None)):
                nutrition.sodium = str(nutritionFields["sodium"]) + "mg"

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