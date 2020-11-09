from flask import jsonify
import json
from models import models
from controllers import base_controller
import time, datetime

def blog_create(params, body): 
    #Initialize
    response = {}
    requiredFields = ["type", "title"]
    postFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        postFields[field] = params.get(field, None)
    if(body == {}):
        response["message"] = "Missing Required Parameters: {}".format(requiredFields)
        status = 400
        return jsonify(response), status

    #Check for Invalid Parameters
    if base_controller.verify(params, requiredFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, requiredFields))
        status = 400
    else:
        #Add Blog to Database
        blog = models.Post(
            post_type="blog",
            title=postFields["title"],
            content=body,
            last_edit=datetime.datetime.now()
        )
        models.db.session.add(blog)
        models.db.session.commit()
        response["message"] = "Blog Post created successfully!"
        status = 200

    return jsonify(response), status

def review_create(params, body): 
    #Initialize
    response = {}
    requiredFields = ["type", "title", "rating"]
    postFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        postFields[field] = params.get(field, None)
    if(body == {}):
        response["message"] = "Missing Required Parameters: {}".format(requiredFields)
        status = 400
        return jsonify(response), status

    #Check for Invalid Parameters
    if base_controller.verify(params, requiredFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, requiredFields))
        status = 400
    else:
        #Add Blog to Database
        review = models.Post(
            post_type="review",
            title=postFields["title"],
            content=body,
            rating=postFields["rating"],
            last_edit=datetime.datetime.now()
        )
        models.db.session.add(review)
        models.db.session.commit()
        response["message"] = "Review Post created successfully!"
        status = 200

    return jsonify(response), status

def recipe_create(params, body): 
    #Initialize
    response = {}
    requiredFields = ["type", "title", "caption"]
    bodyFields = ["ingredients", "instructions"]
    postFields = {}

    decoded_body = json.loads(body.decode())

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        postFields[field] = params.get(field, None)

    for field in bodyFields:
        if(field not in decoded_body.keys()):
            response["message"] = "Missing Required Parameters: {}".format(bodyFields)
            status = 400
            return jsonify(response), status
        postFields[field] = decoded_body.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, requiredFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, requiredFields))
        status = 400
    else:
        #Add Blog to Database
        recipe = models.Post(
            post_type="recipe",
            title=postFields["title"],
            caption=postFields["caption"],
            ingredients=postFields["ingredients"],
            instructions=postFields["instructions"], 
            last_edit=datetime.datetime.now()
        )
        models.db.session.add(recipe)
        models.db.session.commit()
        response["message"] = "Recipe Post created successfully!"
        status = 200

    return jsonify(response), status
