from flask import jsonify
import json
from models import models
from controllers import base_controller, reaction_controller, nutrition_controller
import time, datetime
import requests

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
        
        #make recipe analysis POST request to edamame

        nutrition_api_data = requests.post("https://api.edamam.com/api/nutrition-details?app_id=e8520cc9&app_key=3f16e194023d773558701b51eae413b8", headers={"Content-Type": "application/json"}, data=json.dumps({"title": postFields["title"], "ingr": postFields["ingredients"]}))
        nutrition_api_data = dict(nutrition_api_data.json())
        print(nutrition_api_data)
        #get id of this post recently created post, which will be the recipe_id param
        #... in our nutrition create request
        models.db.session.add(recipe)
        models.db.session.commit()
        post = models.Post.query.order_by(models.Post.post_id.desc()).first()

        #get individual data for calories, fat, carbs,etc from nutrition_api_data and 
        # then put them all in a dict, pass this dict into nutrition_controller.create(...)

        optional_nutrition_fields = ["FAT", "FASAT", "FATRN", "CHOCDF", "FIBTG", "SUGAR", "PROCNT", "CHOLE", "NA"]


        '''
        nutrition_info_dict = {
                "recipe_id" : post.post_id,
                "calories" : str(nutrition_api_data["calories"]),
                "fat" : str(nutrition_api_data["totalNutrients"]["FAT"]["quantity"]),
                "sat_fat" : str(nutrition_api_data["totalNutrients"]["FASAT"]["quantity"]),
                "trans_fat" : str(nutrition_api_data["totalNutrients"]["FATRN"]["quantity"]),
                "carbs" : str(nutrition_api_data["totalNutrients"]["CHOCDF"]["quantity"]),
                "fiber" : str(nutrition_api_data["totalNutrients"]["FIBTG"]["quantity"]),
                "sugar" : str(nutrition_api_data["totalNutrients"]["SUGAR"]["quantity"]),
                "protein" : str(nutrition_api_data["totalNutrients"]["PROCNT"]["quantity"]),
                "chol" : str(nutrition_api_data["totalNutrients"]["CHOLE"]["quantity"]),
                "sodium" : str(nutrition_api_data["totalNutrients"]["NA"]["quantity"])
        }
        '''

        nutrition_info_dict = {
            "recipe_id" : post.post_id,
            "calories" : nutrition_api_data["calories"]
        }

        for element in nutrition_api_data["totalNutrients"]:
            print(element)
            if element in optional_nutrition_fields:
                nutrition_info_dict[str(nutrition_api_data["totalNutrients"][element]["label"]).lower()] = str(nutrition_api_data["totalNutrients"][element]["quantity"])

        
        #Create nutrition object in nutrition db that corresponds to this recipe's nutri
        #... details from Edamam api call
        print(nutrition_info_dict)

        nutrition_return = nutrition_controller.create(nutrition_info_dict) 

        print(nutrition_return)




        response["message"] = "Recipe Post created successfully!"
        status = 200

    
    return jsonify(response), status
    #return str(nutrition_api_data), status

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
            response["user_id"] = post.user_id
            response["image_url"] = post.image_url
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "Post cannot be found"
            status = 200

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
            "reacted_users" : users,
            "image_url" : post.image_url
        }
    status = 200

    return jsonify(response), status

def blog_update(params, body):
    #Initialize
    response = {}
    requiredFields = ["post_id", "type", "title", "user_id"]
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
            post.post_type = postFields["type"]
            post.title = postFields["title"]
            post.content = body.decode()
            post.last_edit = datetime.datetime.now()
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
    requiredFields = ["post_id", "type", "title", "rating", "user_id"]
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
            post.post_type = postFields["type"]
            post.title = postFields["title"]
            post.content = body.decode()
            post.rating = postFields["rating"]
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

def recipe_update(params, body):
    #Initialize
    response = {}
    requiredFields = ["post_id", "type", "title", "caption", "user_id", "image_url"]
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
    requiredFields = ["post_id", "user_id"]
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





