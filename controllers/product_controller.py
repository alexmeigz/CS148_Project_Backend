from flask import jsonify
import time, datetime

def create():
    return

def show(id):
    response = {}
    if not id: #missing product id
        response["message"] = "Missing Product ID Parameter"
        status = 400
    else: #valid product id (currently a placeholder)
        response["product_id"] = 0
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