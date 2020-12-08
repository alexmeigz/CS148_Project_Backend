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
    print("Decoded:", decoded_body)

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
        postFields[field] = json.loads(decoded_body.get(field, ""))

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
        
        #make recipe analysis POST request to edamame
        try:
            nutrition_api_data = requests.post("https://api.edamam.com/api/nutrition-details?app_id=e8520cc9&app_key=3f16e194023d773558701b51eae413b8", headers={"Content-Type": "application/json"}, data=json.dumps({"title": postFields["title"], "ingr": postFields["ingredients"]}))
            nutrition_api_data = dict(nutrition_api_data.json())
        except:
            response["message"] = "Error analyzing nutrition"
            status = 400
            return jsonify(response), status
       
        #get id of this post recently created post, which will be the recipe_id param
        #... in our nutrition create request
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
            if element in optional_nutrition_fields:
                nutrition_info_dict[str(nutrition_api_data["totalNutrients"][element]["label"]).lower()] = str(nutrition_api_data["totalNutrients"][element]["quantity"])

        
        #Create nutrition object in nutrition db that corresponds to this recipe's nutri
        #... details from Edamam api call

        nutrition_return = nutrition_controller.create(nutrition_info_dict) 




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

            #Nutrition
            nutrition_facts = models.Nutrition.query.filter_by(recipe_id=post.post_id).first()

            if nutrition_facts:
                response["calories"] = nutrition_facts.calories
                response["carbs"] = nutrition_facts.carbs
                response["cholesterol"] = nutrition_facts.cholesterol
                response["fat"] = nutrition_facts.fat
                response["fiber"] = nutrition_facts.fiber
                response["nutrition_id"] = nutrition_facts.nutrition_id
                response["protein"] = nutrition_facts.protein
                response["saturated"] = nutrition_facts.saturated
                response["sodium"] = nutrition_facts.sodium
                response["sugars"] = nutrition_facts.sugars
                response["trans"] = nutrition_facts.trans
            else:
                response["calories"] = None
                response["carbs"] = None
                response["cholesterol"] = None
                response["fat"] = None
                response["fiber"] = None
                response["nutrition_id"] = None
                response["protein"] = None
                response["saturated"] = None
                response["sodium"] = None
                response["sugars"] = None
                response["trans"] = None      
            
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
            error_response = {}
            error_response["message"] = "Associated user with post {} cannot be found".format(post.post_id)
            status = 400
            return jsonify(error_response), status

        reactions = models.Reaction.query.filter_by(post_id=post.post_id).all()
        users = list()

        comments = models.Comment.query.filter_by(post_id=post.post_id).all()

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
            "comments" : len(comments),
            "image_url" : post.image_url
        }

        #Nutrition
        nutrition_facts = models.Nutrition.query.filter_by(recipe_id=post.post_id).first()

        if nutrition_facts:
            response[post.post_id]["calories"] = nutrition_facts.calories
            response[post.post_id]["carbs"] = nutrition_facts.carbs
            response[post.post_id]["cholesterol"] = nutrition_facts.cholesterol
            response[post.post_id]["fat"] = nutrition_facts.fat
            response[post.post_id]["fiber"] = nutrition_facts.fiber
            response[post.post_id]["nutrition_id"] = nutrition_facts.nutrition_id
            response[post.post_id]["protein"] = nutrition_facts.protein
            response[post.post_id]["saturated"] = nutrition_facts.saturated
            response[post.post_id]["sodium"] = nutrition_facts.sodium
            response[post.post_id]["sugars"] = nutrition_facts.sugars
            response[post.post_id]["trans"] = nutrition_facts.trans
        else:
            response[post.post_id]["calories"] = None
            response[post.post_id]["carbs"] = None
            response[post.post_id]["cholesterol"] = None
            response[post.post_id]["fat"] = None
            response[post.post_id]["fiber"] = None
            response[post.post_id]["nutrition_id"] = None
            response[post.post_id]["protein"] = None
            response[post.post_id]["saturated"] = None
            response[post.post_id]["sodium"] = None
            response[post.post_id]["sugars"] = None
            response[post.post_id]["trans"] = None      

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





