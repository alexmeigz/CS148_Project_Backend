import os, json
from flask import Flask, request, jsonify, make_response
from controllers import product_controller, post_controller, appl_controller, user_controller, report_controller, nutrition_controller, reaction_controller, order_controller, comment_controller
from models import models
from flask_login import current_user, login_user, logout_user
from flask_login import LoginManager
from werkzeug.urls import url_parse
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
DEBUG=True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
models.db.init_app(app)

# ------------------------------ CORS ------------------------------
@app.after_request
def after_request_func(response):
    if DEBUG:
        print("in after_request")
    origin = request.headers.get('Origin')
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Headers', 'x-csrf-token')
        response.headers.add('Access-Control-Allow-Methods',
                            'GET, POST, OPTIONS, PUT, PATCH, DELETE')
        if origin:
            response.headers.add('Access-Control-Allow-Origin', origin)
    else:
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        if origin:
            response.headers.add('Access-Control-Allow-Origin', origin)

    return response

# ------------------------------ PRODUCT URLS ------------------------------
@app.route('/api/product/', methods=['POST'])
def createProduct():
    if(request.args.get("test", None)):
        return product_controller.add_test_data()
    else:
        return product_controller.create(request.args)

@app.route('/api/product/', methods=['GET'])
def showProduct():
    if(request.args.get("display_all", None)):
        return product_controller.display_all(request.args)
    else:
        return product_controller.show(request.args)

@app.route('/api/product/', methods=['PATCH'])
def updateProduct():
    return product_controller.update(request.args)

@app.route('/api/product/', methods=['DELETE'])
def deleteProduct():
    return product_controller.delete(request.args)

# ------------------------------ APPLICATION URLS ------------------------------
@app.route('/api/application/', methods=['POST'])
def createApplication():
    return appl_controller.create(request.args)

@app.route('/api/application/', methods=['GET'])
def showApplication():
    if(request.args.get("display_all", None)):
        return appl_controller.display_all(request.args)
    else:
        return appl_controller.show(request.args)

@app.route('/api/application/', methods=['PATCH'])
def updateApplication():
    return appl_controller.update(request.args)

@app.route('/api/application/', methods=['DELETE'])
def deleteApplication():
    return appl_controller.delete(request.args)

# ------------------------------ POST URLS ------------------------------
@app.route('/api/post/', methods=['POST'])
def createPost():
    if(not request.args.get("type", None)):
        return {"message" : "Missing Required Parameter: type"}, 400
    elif(request.args["type"].lower() == "blog"):
        return post_controller.blog_create(request.args, request.data)
    elif(request.args["type"].lower() == "review"):
        return post_controller.review_create(request.args, request.data)
    elif(request.args["type"].lower() == "recipe"):
        return post_controller.recipe_create(request.args, request.data)
    else:
        return {"message" : "Parameter type must have value 'post', 'recipe', or 'review'"}, 400

@app.route('/api/post/', methods=['GET'])
def showPost():
    if(request.args.get("display_all", None)):
        return post_controller.display_all(request.args)
    else:
        return post_controller.show(request.args)

@app.route('/api/post/', methods=['PATCH'])
def updatePost():
    if(not request.args.get("post_type", None)):
        return {"message" : "Missing Required Parameter: type"}, 400
    elif(request.args["post_type"].lower() == "blog"):
        return post_controller.blog_update(request.args, request.data)
    elif(request.args["post_type"].lower() == "review"):
        return post_controller.review_update(request.args, request.data)
    elif(request.args["post_type"].lower() == "recipe"):
        return post_controller.recipe_update(request.args, request.data)
    else:
        return {"message" : "Parameter post_type must have value 'post', 'recipe', or 'review'"}, 400

@app.route('/api/post/', methods=['DELETE'])
def deleteApp():
    return post_controller.delete(request.args)

# ------------------------------ USER URLS ------------------------------
@app.route('/api/user/', methods=['POST'])
def createUser(): 
    return user_controller.create(request.args)

@app.route('/api/user/', methods=['GET'])
def showUser():
    if(request.args.get("login", None)):
        return user_controller.login(request.args)
    elif(request.args.get("display_all", None)):
        return user_controller.display_all(request.args)
    else:
        return user_controller.show(request.args)

@app.route('/api/user/', methods=['PATCH'])
def updateUser():
    return user_controller.update(request.args)

@app.route('/api/user/', methods=['DELETE'])
def deleteUser():
    return user_controller.delete(request.args)

# ------------------------------ REPORT URLS ------------------------------
@app.route('/api/report/', methods=['POST'])
def createReport(): 
    return report_controller.create(request.args, request.data)

@app.route('/api/report/', methods=['GET'])
def showReport():
    if(request.args.get("show", None)):
        return report_controller.show(request.args)
    elif(request.args.get("display_all", None)):
        return report_controller.display_all(request.args)
    else:
        return report_controller.show(request.args)

@app.route('/api/report/', methods=['PATCH'])
def updateReport():
    return report_controller.update(request.args, request.data)

@app.route('/api/report/', methods=['DELETE'])
def deleteReport():
    return report_controller.delete(request.args)

# ------------------------------ NUTRITION URLS ------------------------------
@app.route('/api/nutrition/', methods=['POST'])
def createNutrition(): 
    return nutrition_controller.create(request.args)

@app.route('/api/nutrition/', methods=['GET'])
def showNutrition():
    if(request.args.get("show", None)):
        return nutrition_controller.show(request.args)
    elif(request.args.get("display_all", None)):
        return nutrition_controller.display_all(request.args)
    else:
        return nutrition_controller.show(request.args)

@app.route('/api/nutrition/', methods=['PATCH'])
def updateNutrition():
    return nutrition_controller.update(request.args)

@app.route('/api/nutrition/', methods=['DELETE'])
def deleteNutrition():
    return nutrition_controller.delete(request.args)

# ------------------------------ REACTION URLS ------------------------------
@app.route('/api/reaction/', methods=['POST'])
def createReaction(): 
    return reaction_controller.create(request.args)

@app.route('/api/reaction/', methods=['GET'])
def showReaction():
    if request.args.get("post_id", None):
        return reaction_controller.display_all(request.args)
    else:
        return reaction_controller.show(request.args)

@app.route('/api/reaction/', methods=['DELETE'])
def deleteReaction():
    return reaction_controller.delete(request.args)

# ------------------------------ ORDER URLS ------------------------------
@app.route('/api/order/', methods=['POST'])
def createOrder(): 
    return order_controller.create(request.args)

@app.route('/api/order/', methods=['GET'])
def showOrder():
    if request.args.get("display_all", None):
        return order_controller.display_all(request.args)
    else:
        return order_controller.show(request.args)

@app.route('/api/order/', methods=['PATCH'])
def updateOrder(): 
    return order_controller.update(request.args)

@app.route('/api/order/', methods=['DELETE'])
def deleteOrder():
    return order_controller.delete(request.args)

# ------------------------------ COMMENT URLS ------------------------------
@app.route('/api/comment/', methods=['POST'])
def createComment():
    return comment_controller.create(request.args)

@app.route('/api/comment/', methods=['GET'])
def showComment():
    if(request.args.get("display_all", None)):
        return comment_controller.display_all(request.args)
    else:
        return comment_controller.show(request.args)

@app.route('/api/comment/', methods=['DELETE'])
def deleteComment():
    return comment_controller.delete(request.args)

# ------------------------------ ROOT URL ------------------------------
@app.route('/')
def index():
    return "<h1> Welcome to the Masterchef Kitchen! </h1>", 200

# ------------------------------ MAIN ------------------------------
def main():
    localport = int(os.getenv("PORT", 8118))
    app.config['DEBUG'] = True
    app.run(threaded=True, host='0.0.0.0', port=localport)

if __name__ == '__main__':
    main()

    
    
    
    
