''' 
    This file is based off of this tutorial: https://stackabuse.com/deploying-a-flask-application-to-heroku/ 
    Author: Chandra Krintz, 
    License: UCSB BSD -- see LICENSE file in this repository
'''

import os, json
from flask import Flask, request, jsonify, make_response
from controllers import product_controller
from models import models

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
    %(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
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
    '''
    POST PARAMS:
    product_name: str (required)
    subscription: bool (required)
    price: float (required)
    location: str (optional)
    frequency: int (optional)
    
    RESPONSE: (if successful)
    {
        "message": "Product created successfully!"
    }
    '''
    return product_controller.create(request.args)

@app.route('/api/product/', methods=['GET'])
def showProduct():
    '''
    GET PARAMS:
    id = product_id (required)
    
    RESPONSE: (if successful) 
    {
        "frequency": str(datetime.timedelta),
        "list_date": datetime,
        "location": str,
        "nutrition_id": int,
        "price": str (includes currency symbol),
        "product_id": int,
        "product_name": str,
        "subscription": bool
    }   
    '''
    return product_controller.show(request.args)

@app.route('/api/product/', methods=['PATCH'])
def updateProduct():
    '''
    PATCH PARAMS:
    id = product_id (required)
    product_name: str (required)
    subscription: bool (required)
    price: float (required)
    location: str (optional)
    frequency: int (optional)
    
    RESPONSE: (if successful) 
    {
        "message": "Product sucessfully updated"
    }   
    '''
    return product_controller.update(request.args)

@app.route('/api/product/', methods=['DELETE'])
def deleteProduct():
    '''
    DELETE PARAMS:
    id = product_id (required)
    
    RESPONSE: (if successful) 
    {
        "message": "Product sucessfully removed"
    }   
    '''
    return product_controller.delete(request.args)

# Set the base route to be the react index.html
@app.route('/')
def index():
    return "<h1> Welcome to the Masterchef Kitchen !!</h1>", 200

    #use this instead if linking to a raact app on the same server
    #make sure and xupdate the app = Flask(...) line above for the same
    #return app.send_static_file('index.html') 

def main():
    '''The threaded option for concurrent accesses, 0.0.0.0 host says listen to all network interfaces (leaving this off changes this to local (same host) only access, port is the port listened on -- this must be open in your firewall or mapped out if within a Docker container. In Heroku, the heroku runtime sets this value via the PORT environment variable (you are not allowed to hard code it) so set it from this variable and give a default value (8118) for when we execute locally.  Python will tell us if the port is in use.  Start by using a value > 8000 as these are likely to be available.
    '''
    localport = int(os.getenv("PORT", 8118))
    app.config['DEBUG'] = True
    app.run(threaded=True, host='0.0.0.0', port=localport)

if __name__ == '__main__':
    main()