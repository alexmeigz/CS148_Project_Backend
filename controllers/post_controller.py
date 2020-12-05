from flask import jsonify
import json
from models import models
from controllers import base_controller, reaction_controller
import time, datetime

def blog_create(params, body): 
    #Initialize
    response = {}
    requiredFields = ["type", "title", "user_id"]
    optionalFields = ["image_url"]
    allFields = requiredFields + optionalFields
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

    #Check for Optional Fields
    for field in optionalFields:
        postFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        if body.decode().strip() == "":
            response["message"] = "Request content cannot be null"
            status = 400
            return jsonify(response), status
            
        #Add Blog to Database
        blog = models.Post(
            post_type="blog",
            title=postFields["title"],
            content=body.decode(),
            user_id=postFields["user_id"],
            image_url=postFields["image_url"],
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
    requiredFields = ["type", "title", "rating", "user_id"]
    optionalFields = ["image_url"]
    allFields = requiredFields + optionalFields
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

    #Check for Optional Fields
    for field in optionalFields:
        postFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Check for valid type
        try:
            postFields["rating"] = float(postFields["rating"])
        except:
            response["message"] = "Request has invalid parameter type"
            status = 400
            return jsonify(response), status

        #Check for valid rating
        if not (1 <= postFields["rating"] <= 5):
            response["message"] = "Request has invalid rating (must be from 1 to 5"
            status = 400
            return jsonify(response), status

        if body.decode().strip() == "":
            response["message"] = "Request content cannot be null"
            status = 400
            return jsonify(response), status
            
        #Add Blog to Database
        review = models.Post(
            post_type="review",
            title=postFields["title"],
            content=body.decode(),
            rating=postFields["rating"],
            user_id=postFields["user_id"],
            image_url=postFields["image_url"],
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
    requiredFields = ["type", "title", "caption", "user_id", "image_url"]
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
            user_id=postFields["user_id"],
            image_url=postFields["image_url"],
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

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Query for Product
        post = models.Post.query.filter_by(post_id=postFields["post_id"]).first()

        if post is not None:
            user = models.User.query.filter_by(user_id=post.user_id).first()
        
            if user is None:
                #Query Unsuccessful
                response["message"] = "Associated user cannot be found"
                status = 400
                return jsonify(response), status

            #Reactions
            reactions = models.Reaction.query.filter_by(post_id=post.post_id).all()
            users = list()

            for reaction in reactions:
                users.append(reaction.user_id)

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
            response["username"] = user.username
            response["user_id"] = post.user_id
            response["image_url"] = post.image_url
            response["reacted_users"] = users
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "Post cannot be found"
            status = 400

    return jsonify(response), status

def display_all(params):
    q = models.Post.query
    
    if(params.get("user_id", None != None)):
        q = q.filter_by(user_id=params["user_id"])

    if(params.get("title", None != None)):
        q = q.filter(models.Post.title.contains(params["title"]))
    
    if params.get("post_type", None) != None:
        q = q.filter_by(post_type=params["post_type"])
    else:
        types = list()
        if params.get("recipe", None) == "true":
            types.append("recipe")
        if params.get("review", None) == "true":
            types.append("review")
        if params.get("blog", None) == "true":
            types.append("blog")
        if types:
            q = q.filter(models.Post.post_type.in_(types))
      
    posts = q.all()
    
    response = {}

    for post in posts:
        user = models.User.query.filter_by(user_id=post.user_id).first()

        if user is None:
            #Query Unsuccessful
            response["message"] = "Associated user with post {} cannot be found".format(post.post_id)
            status = 400
            return jsonify(response), status

        reactions = models.Reaction.query.filter_by(post_id=post.post_id).all()
        users = list()

        for reaction in reactions:
            users.append(reaction.user_id)

        response[post.post_id] = {
            "post_id" : post.post_id,
            "post_type" : post.post_type,
            "title" : post.title,
            "content" : post.content,
            "rating" : post.rating,
            "caption" : post.caption,
            "ingredients" : post.ingredients,
            "instructions" : post.instructions,
            "last_edit" : post.last_edit,
            "user_id" : post.user_id,
            "username" : user.username,
            "reacted_users" : users,
            "image_url" : post.image_url
        }
    status = 200

    return jsonify(response), status

def blog_update(params, body):
    #Initialize
    response = {}
    requiredFields = ["post_id", "post_type", "title"]
    optionalFields = ["image_url"]
    allFields = requiredFields + optionalFields
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
            #Update Product
            post.post_type = postFields["post_type"]
            post.title = postFields["title"]
            post.content = body.decode()
            post.last_edit = datetime.datetime.now()
            
            if postFields.get("image_url") != None:
                post.image_url = postFields["image_url"]
            
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
    requiredFields = ["post_id", "post_type", "title", "rating"]
    optionalFields = ["image_url"]
    allFields = requiredFields + optionalFields
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
            #Update Product
            post.post_type = postFields["post_type"]
            post.title = postFields["title"]
            post.content = body.decode()
            post.rating = postFields["rating"]
            post.last_edit = datetime.datetime.now()

            if postFields.get("image_url") != None:
                post.image_url = postFields["image_url"]

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
    requiredFields = ["post_id", "post_type", "title", "caption", "image_url"]
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
            post.post_type = postFields["post_type"]
            post.title = postFields["title"]
            post.caption = postFields["caption"]
            post.ingredients = postFields["ingredients"]
            post.instructions = postFields["instructions"]
            post.image_url = postFields["image_url"]
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





