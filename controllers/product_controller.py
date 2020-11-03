from flask import jsonify
from models import models
from controllers import base_controller
import time, datetime

def create(params): 
    #Initialize
    response = {}
    requiredFields = ["vendor_id", "product_name", "subscription", "price"]
    optionalFields = ["location", "frequency"]
    allFields = requiredFields + optionalFields
    productFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        productFields[field] = params.get(field, None)
        
    #Check for Optional Fields
    for field in optionalFields:
        if field == "frequency":
            productFields[field] = params.get(field, 0)
        else:
            productFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Check for Numerical Price and Frequency
        try:
            productFields["price"] = float(productFields["price"])
            productFields["vendor_id"] = int(productFields["vendor_id"])
            productFields["frequency"] = int(productFields["frequency"])
        except:
            response["message"] = "Request has incorrect parameter type"
            status = 400
            return jsonify(response), status

        #Add Product to Database
        productFields["subscription"] = productFields["subscription"] == "True"
        product = models.Product(
            vendor_id=productFields["vendor_id"],
            name=productFields["product_name"],
            subscription=productFields["subscription"],
            price=productFields["price"],
            location=productFields["location"],
            frequency=datetime.timedelta(days=productFields["frequency"]),
            list_date=datetime.date.today()
            )
        models.db.session.add(product)
        models.db.session.commit()
        response["message"] = "Product created successfully!"
        status = 200
  
    return jsonify(response), status

def show(params):
    #Initialize
    response = {}
    requiredFields = ["id"]
    optionalFields = []
    allFields = requiredFields + optionalFields
    productFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        productFields[field] = params.get(field, None)
        
    #Check for Optional Fields
    for field in optionalFields:
        productFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Query for Product
        product = models.Product.query.filter_by(id=productFields["id"]).first()
        
        if product is not None:
            #Query Successful
            response["id"] = product.id
            response["product_name"] = product.name
            response["subscription"] = product.subscription
            response["frequency"] = str(product.frequency)
            response["price"] = product.price
            response["list_date"] = str(product.list_date)
            response["location"] = product.location
            response["nutrition_id"] = product.nutrition_id
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "Product cannot be found"
            status = 200

    return jsonify(response), status

def update(params):
    #Initialize
    response = {}
    requiredFields = ["id", "product_name", "subscription", "price"]
    optionalFields = ["location", "frequency"]
    allFields = requiredFields + optionalFields
    productFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        productFields[field] = params.get(field, None)

    #Check for Optional Fields
        for field in optionalFields:
            productFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Query for Product
        product = models.Product.query.filter_by(id=productFields["id"]).first()     

        if product is not None:
            #Check for Numerical Price and Frequency
            try:
                productFields["price"] = float(productFields["price"])
                productFields["frequency"] = int(productFields["frequency"])
            except:
                response["message"] = "Request has incorrect parameter type"
                status = 400
                return jsonify(response), status

            #Update Product
            product.name = productFields["product_name"]
            product.subscription = productFields["subscription"] == "True"
            product.frequency = datetime.timedelta(days=productFields["frequency"])
            product.price = productFields["price"]
            product.location = productFields["location"]
            models.db.session.commit()
            
            #Query Successful
            response["message"] = "Product successfully updated"
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "Product cannot be found"
            status = 200

    return jsonify(response), status

def delete(params):
    #Initialize
    response = {}
    requiredFields = ["id"]
    optionalFields = []
    allFields = requiredFields + optionalFields
    productFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        productFields[field] = params.get(field, None)
        
    #Check for Optional Fields
    for field in optionalFields:
        productFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Query for Product
        product = models.Product.query.filter_by(id=productFields["id"]).first()
        
        if product is not None:
            #Query Successful
            models.db.session.delete(product)
            models.db.session.commit()
            response["message"] = "Product successfully removed"
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "Product cannot be found"
            status = 200

    return jsonify(response), status