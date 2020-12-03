from flask import jsonify
from models import models
from controllers import base_controller
import time, datetime
from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash


def create(params): 
    #Initialize
    response = {}
    requiredFields = ["product_id", "price", "buyer_id", "seller_id"]
    orderFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        orderFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, requiredFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, requiredFields))
        status = 400
    else:
        try:
            orderFields["price"] = float(orderFields["price"])
        except:
            response["message"] = "Response has invalid parameter type"
            status = 400
            return jsonify(response), status

        #Add User to Database
        order = models.Order(
                product_id=orderFields["product_id"],
                price=orderFields["price"],
                buyer_id=orderFields["buyer_id"],
                seller_id=orderFields["seller_id"],
                status="Pending",
                update_date=datetime.date.today()
            )
        try:
            models.db.session.add(order)
        except:
            response["message"] = "Order already exists."
            status = 400
            return jsonify(response), status

        try:
            buyer = models.User.query.filter_by(user_id=orderFields["buyer_id"]).first()
            buyer.credits -= orderFields["price"]
            models.db.session.commit()
            response["message"] = "Order created successfully!"
            status = 200
        except:
            response["message"] = "Cannot deduct credits from buyer."
            status = 400
    return jsonify(response), status

def show(params):
    #Initialize
    response = {}
    requiredFields = ["order_id"]
    orderFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        orderFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, requiredFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, requiredFields))
        status = 400
    else:
        #Query for User
        order = models.Order.query.filter_by(order_id=orderFields["order_id"]).first()

        if order is not None:
            #Query Successful
            response["order_id"] = order.order_id
            response["product_id"] = order.product_id
            response["price"] = order.price
            response["buyer_id"] = order.buyer_id
            response["seller_id"] = order.seller_id
            response["update_date"] = order.update_date
            response["status"] = order.status
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "Order cannot be found"
            status = 400

    return jsonify(response), status

def display_all(params):
    q = models.Order.query
    if params.get("buyer_id", None) != None:
        q = q.filter_by(buyer_id=params["buyer_id"])
    if params.get("seller_id", None) != None:
        q = q.filter_by(seller_id=params["seller_id"])
    orders = q.all()

    
    response = {}
    for order in orders:
        response[order.order_id] = {
            "order_id" : order.order_id,
            "buyer_id" : order.buyer_id,
            "seller_id" : order.seller_id,
            "product_id" : order.product_id,
            "status" : order.status,
            "price" : order.price,
            "update_date" : order.update_date
        }
    status = 200

    return jsonify(response), status

def update(params):
    #Initialize
    response = {}
    requiredFields = ["order_id", "status"]
    orderFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        orderFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, requiredFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, requiredFields))
        status = 400
    else:
        #Check for valid status
        if orderFields["status"] not in ["Shipped", "Refunded", "Confirmed"]:
            response["message"] = "Invalid status"
            status = 400
            return jsonify(response), status

        #Query for User
        order = models.Order.query.filter_by(order_id=orderFields["order_id"]).first()     

        if order is not None:
            order.status = orderFields["status"]
            order.update_date = datetime.date.today()
        else:
            #Query Unsuccessful
            response["message"] = "Order cannot be found"
            status = 400

        try:
            if orderFields["status"] == "Refunded":
                buyer = models.User.query.filter_by(user_id=order.buyer_id).first()
                buyer.credits += order.price
            elif orderFields["status"] == "Confirmed":
                seller = models.User.query.filter_by(user_id=order.seller_id).first()
                seller.credits += order.price
            models.db.session.commit()
            
            #Query Successful
            response["message"] = "Order successfully updated"
            status = 200
        except:
            #Query Unsuccessful
            response["message"] = "Unsuccessful credit transfer"
            status = 400

    return jsonify(response), status

def delete(params):
    #Initialize
    response = {}
    requiredFields = ["order_id"]
    orderFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        orderFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, requiredFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, requiredFields))
        status = 400
    else:
        #Query for User
        order = models.Order.query.filter_by(order_id=orderFields["order_id"]).first()
        
        if order is not None:
            #Query Successful
            models.db.session.delete(order)
            models.db.session.commit()
            response["message"] = "Order successfully removed"
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "Order cannot be found"
            status = 400

    return jsonify(response), status