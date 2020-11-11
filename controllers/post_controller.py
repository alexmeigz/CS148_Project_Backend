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
        response["message"] = "Missing Required Parameters: {}".format("content")
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
            content=body.decode(),
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
        response["message"] = "Missing Required Parameters: {}".format("content")
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
            content=body.decode(),
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

def show(params):
    #Initialize
    response = {}
    requiredFields = ["post_id"]
    optionalFields = []
    allFields = requiredFields + optionalFields
    postFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        postFields[field] = params.get(field, None)
        
    #Check for Optional Fields
    for field in optionalFields:
        postFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Query for Product
        post = models.Post.query.filter_by(post_id=postFields["post_id"]).first()
        
        if post is not None:
            #Query Successful
            response["post_id"] = post.post_id
            response["post_type"] = post.post_type
            response["title"] = post.title
            response["content"] = post.content
            response["rating"] = post.rating
            response["caption"] = post.caption
            response["ingredients"] = post.ingredients
            response["instructions"] = post.instructions
            response["last_edit"] = post.last_edit
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "Post cannot be found"
            status = 200

    return jsonify(response), status

def display_all(params):
    posts = models.Post.query.all()
    
    response = {}
    for post in posts:
        response[post.post_id] = {
            "post_id" : post.post_id,
            "post_type" : post.post_type,
            "title" : post.title,
            "content" : post.content,
            "rating" : post.rating,
            "caption" : post.caption,
            "ingredients" : post.ingredients,
            "instructions" : post.instructions,
            "last_edit" : post.last_edit
        }
    status = 200

    return jsonify(response), status

def blog_update(params, body):
    #Initialize
    response = {}
    requiredFields = ["post_id", "type", "title"]
    postFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        postFields[field] = params.get(field, None)
    if(body == {}):
        response["message"] = "Missing Required Parameters: {}".format("content")
        status = 400
        return jsonify(response), status

    #Check for Invalid Parameters
    if base_controller.verify(params, requiredFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, requiredFields))
        status = 400
    else:
        #Query for Product
        post = models.Post.query.filter_by(post_id=postFields["post_id"]).first()     

        if post is not None:
            #Update Product
            post.post_type = postFields["type"]
            post.title = postFields["title"]
            post.content = body.decode()
            post.last_edit = datetime.datetime.now()
            models.db.session.commit()
            
            #Query Successful
            response["message"] = "Post successfully updated"
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "Post cannot be found"
            status = 200

    return jsonify(response), status

def review_update(params, body):
    #Initialize
    response = {}
    requiredFields = ["post_id", "type", "title", "rating"]
    postFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        postFields[field] = params.get(field, None)
    if(body == {}):
        response["message"] = "Missing Required Parameters: {}".format("content")
        status = 400
        return jsonify(response), status

    #Check for Invalid Parameters
    if base_controller.verify(params, requiredFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, requiredFields))
        status = 400
    else:
        #Query for Product
        post = models.Post.query.filter_by(post_id=postFields["post_id"]).first()     

        if post is not None:
            #Update Product
            post.post_type = postFields["type"]
            post.title = postFields["title"]
            post.content = body.decode()
            post.rating = postFields["rating"]
            post.last_edit = datetime.datetime.now()
            models.db.session.commit()
            
            #Query Successful
            response["message"] = "Post successfully updated"
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "Post cannot be found"
            status = 200

    return jsonify(response), status

def recipe_update(params, body):
    #Initialize
    response = {}
    requiredFields = ["post_id", "type", "title", "caption"]
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
    if(body == {}):
        response["message"] = "Missing Required Parameters: {}".format("content")
        status = 400
        return jsonify(response), status

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
        #Query for Product
        post = models.Post.query.filter_by(post_id=postFields["post_id"]).first()     

        if post is not None:
            #Update Product
            post.post_type = postFields["type"]
            post.title = postFields["title"]
            post.caption = postFields["caption"]
            post.ingredients = postFields["ingredients"]
            post.instructions = postFields["instructions"]
            post.last_edit = datetime.datetime.now()
            models.db.session.commit()
            
            #Query Successful
            response["message"] = "Post successfully updated"
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "Post cannot be found"
            status = 200

    return jsonify(response), status

def delete(params):
    #Initialize
    response = {}
    requiredFields = ["post_id"]
    optionalFields = []
    allFields = requiredFields + optionalFields
    postFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        postFields[field] = params.get(field, None)
        
    #Check for Optional Fields
    for field in optionalFields:
        postFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Query for Product
        post = models.Post.query.filter_by(post_id=postFields["post_id"]).first()
        
        if post is not None:
            #Query Successful
            models.db.session.delete(post)
            models.db.session.commit()
            response["message"] = "Post successfully removed"
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "Post cannot be found"
            status = 200

    return jsonify(response), status





