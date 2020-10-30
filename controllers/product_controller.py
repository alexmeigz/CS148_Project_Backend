from flask import jsonify
from controllers import base_controller
import time, datetime

def create(params): 
    response = {}
    requiredFields = ["product_name", "subscription", "price"]
    optionalFields = ["location"]
    allFields = requiredFields + optionalFields
    
    productFields = {}
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters (product_name, subscription, price)"
            status = 400
            return response
        productFields[field] = params.get(field, None)
        
    for field in optionalFields:
        productFields[field] = params.get(field, None)

    if base_controller.verify(params, allFields): #passed invalid parameter
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        try:
            productFields["price"] = float(productFields["price"])
            response["message"] = "Product created successfully!"
            status = 200
        except:
            response["message"] = "Price Parameter not a Float type"
            status = 400
  
    return response

def show(id):
    response = {}
    if not id: #missing product id
        response["message"] = "Missing Product ID Parameter"
        status = 400
    else: #valid product id (currently a placeholder)
        response["product_id"] = 0
        response["product_name"] = "Avocado Toast"
        response["subscription"] = False
        response["frequency"] = str(datetime.timedelta(weeks=1))
        response["price"] = "$100"
        response["list_date"] = datetime.date.today()
        response["location"] = "Santa Barbara"
        response["nutrition_id"] = 0
        status = 200

    # Return the response in json format with status code
    return jsonify(response), status

def update():
    return

def delete():
    return