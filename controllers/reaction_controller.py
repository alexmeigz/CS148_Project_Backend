from flask import jsonify
from models import models
from controllers import base_controller
import time, datetime

def create(params): 
    #Initialize
    response = {}
    requiredFields = ["user_id", "post_id"]
    reactionFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        reactionFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, requiredFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, requiredFields))
        status = 400
    else:
        #Check for Numerical IDs
        try:
            reactionFields["post_id"] = int(reactionFields["post_id"])
            reactionFields["user_id"] = int(reactionFields["user_id"])
        except:
            response["message"] = "Request has incorrect parameter type"
            status = 400
            return jsonify(response), status

        #Add Product to Database
        reaction = models.Reaction(
            user_id=reactionFields["user_id"],
            post_id=reactionFields["post_id"],
            )
        models.db.session.add(reaction)
        models.db.session.commit()
        response["message"] = "Reaction created successfully!"
        status = 200
  
    return jsonify(response), status

def show(params):
    #Initialize
    response = {}
    requiredFields = ["reaction_id"]
    reactionFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        reactionFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, requiredFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, requiredFields))
        status = 400
    else:
        #Query for Reaction
        reaction = models.Reaction.query.filter_by(reaction_id=reactionFields["reaction_id"]).first()
        
        if reaction is not None:
            #Query Successful
            response["reaction_id"] = reaction.reaction_id
            response["user_id"] = reaction.user_id
            response["post_id"] = reaction.post_id
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "Reaction cannot be found"
            status = 200

    return jsonify(response), status

def display_all(params):
    #Initialize
    response = {}
    requiredFields = ["post_id"]
    reactionFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        reactionFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, requiredFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, requiredFields))
        status = 400
    else:
        #Query for Reaction
        reactions = models.Reaction.query.filter_by(post_id=reactionFields["post_id"]).all()
        
        for reaction in reactions:
            response[reaction.reaction_id] = {
                "reaction_id" : reaction.reaction_id,
                "user_id" : reaction.user_id,
                "post_id" : reaction.post_id
            }
    
        status = 200
    return jsonify(response), status

def delete(params):
    #Initialize
    response = {}
    requiredFields = ["reaction_id"]
    reactionFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        reactionFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, requiredFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, requiredFields))
        status = 400
    else:
        #Query for Product
        reaction = models.Reaction.query.filter_by(reaction_id=reactionFields["reaction_id"]).first()
        
        if reaction is not None:
            #Query Successful
            models.db.session.delete(reaction)
            models.db.session.commit()
            response["message"] = "Reaction successfully removed"
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "Reaction cannot be found"
            status = 200

    return jsonify(response), status