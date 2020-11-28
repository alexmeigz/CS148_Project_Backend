# This file is based off of this tutorial: https://stackabuse.com/deploying-a-flask-application-to-heroku/ 
# #Author: Chandra Krintz, 
# License: UCSB BSD -- see LICENSE file in this repository


import os, json
from flask import Flask, request, jsonify, make_response
from controllers import product_controller, post_controller, appl_controller, user_controller, report_controller, nutrition_controller
from models import models
from flask_login import current_user, login_user, logout_user
from flask_login import LoginManager
from werkzeug.urls import url_parse

#use this if linking to a reaact app on the same server
#app = Flask(__name__, static_folder='./build', static_url_path='/')
app = Flask(__name__)
DEBUG=True
POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'cs148db',
    'host': 'localhost',
    'port': '5432',
}

#For Production:
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rfshnkukompizc:d1ceeaebb80d23172c143eecc4e446c9cacba1877862b7be3acf1714c8aea51d@ec2-3-210-178-167.compute-1.amazonaws.com:5432/d5k9aac8pmgho9'

#For Testing:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
   %(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

login = LoginManager(app) # for logging in
login.login_view = 'login'

models.db.init_app(app)

### CORS section
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
### end CORS section

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
    if(not request.args.get("type", None)):
        return {"message" : "Missing Required Parameter: type"}, 400
    elif(request.args["type"].lower() == "blog"):
        return post_controller.blog_update(request.args, request.data)
    elif(request.args["type"].lower() == "review"):
        return post_controller.review_update(request.args, request.data)
    elif(request.args["type"].lower() == "recipe"):
        return post_controller.recipe_update(request.args, request.data)
    else:
        return {"message" : "Parameter type must have value 'post', 'recipe', or 'review'"}, 400

@app.route('/api/post/', methods=['DELETE'])
def deleteApp():
    return post_controller.delete(request.args)
###End of Post routes ###

## Start of User routes

@app.route('/api/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login')) #FLAG: if login failed, redirect to login page, 
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page) #FLAG: if login success, redirect to the original page
    return render_template('login.html', title='Sign In', form=form)

@app.route('/api/logout/')
def logout():
    logout_user()
    return redirect(url_for('index')) #FLAG: redirect to main index page

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


### End of User routes ###

### Start of Report routes ###
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

### End of Report routes ###

### Start of Nutrition routes ###
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

### End of Nutrition routes ###

# Set the base route to be the react index.html
@app.route('/')
def index():
    return "<h1> Welcome to the Masterchef Kitchen !!</h1>", 200

    #use this instead if linking to a raact app on the same server
    #make sure and xupdate the app = Flask(...) line above for the same
    #return app.send_static_file('index.html') 

def main():
    #The threaded option for concurrent accesses, 0.0.0.0 host says listen to all network interfaces (leaving this off changes this to local (same host) only access, port is the port listened on -- this must be open in your firewall or mapped out if within a Docker container. In Heroku, the heroku runtime sets this value via the PORT environment variable (you are not allowed to hard code it) so set it from this variable and give a default value (8118) for when we execute locally.  Python will tell us if the port is in use.  Start by using a value > 8000 as these are likely to be available.
 
    localport = int(os.getenv("PORT", 8118))
    app.config['DEBUG'] = True
    app.run(threaded=True, host='0.0.0.0', port=localport)

if __name__ == '__main__':
    main()

    
    
    
    
