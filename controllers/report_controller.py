from flask import jsonify
from models import models
from controllers import base_controller
import time, datetime
from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash


def create(params): 
    #Initialize
    response = {}
    requiredFields = ["userReporter_id", "reportedUser_id", "reportText"]
    optionalFields = []
    allFields = requiredFields + optionalFields
    userFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        userFields[field] = params.get(field, None)
        
    #Check for Optional Fields
    for field in optionalFields:
        if field == "frequency":
            userFields[field] = params.get(field, 0)
        else:
            userFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    '''else:
        if userFields["account_type"] not in ["Normal", "Home",  "Restaurant", "Admin"]:
            print(userFields["account_type"])
            response["message"] = "account_type must be one of the following: {}".format(["Normal", "Home",  "Restaurant", "Admin"])
            status = 400
            return jsonify(response), status'''

        #Add User to Database
        report = models.Report(
            userReporter_id=userFields["userReporter_id"],
            reportedUser_id=userFields["reportedUser_id"],
            reportText=userFields["reportText"],
            reportDate=datetime.date.today()
            )
        try:
            models.db.session.add(report)
            models.db.session.commit()
            response["message"] = "Report submitted successfully!"
            status = 200
        except:
            response["message"] = "Report couldn't be submitted."
            status = 400
  
    return jsonify(response), status


def show(params):
    #Initialize
    response = {}
    requiredFields = ["report_id"]
    optionalFields = []
    allFields = requiredFields + optionalFields
    applFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        applFields[field] = params.get(field, None)
        
    #Check for Optional Fields
    for field in optionalFields:
        applFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Query for Application
        report = models.Report.query.filter_by(report_id=applFields["report_id"]).first()
        
        if application is not None:
            #Query Successful
            response["report_id"] = report.report_id
            response["userReporter_id"] = report.userReporter_id
            response["reportedUser_id"] = report.reportedUser_id
            response["reportText"] = report.reportText
            response["reportDate"] = str(report.reportDate)
            response["message"] = "Report found"
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "Report cannot be found"
            status = 200

    return jsonify(response), status


##finished up to here

def display_all(params):
    applications = models.Application.query.all()
    response = {}
    for application in applications:
        response[application.id] = {
            "applsDate": str(application.applsDate),
            "busLocation": application.busLocation,
            "application_id": application.id,
            "user_id": application.user_id,
            "restName": application.restName,
            "reason": application.reason,
            "vendorType": application.vendorType
        }
    status = 200
    return jsonify(response), status

def update(params):
    #Initialize
    response = {}
    requiredFields = ["id", "user_id", "restName", "vendorType", "reason"]
    optionalFields = ["busLocation"]
    allFields = requiredFields + optionalFields
    applFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        applFields[field] = params.get(field, None)

    #Check for Optional Fields
        for field in optionalFields:
            applFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Query for Product
        application = models.Application.query.filter_by(id=applFields["id"]).first()     

        if application is not None:
            #Check for Numerical Price and Frequency
            try:
                applFields["user_id"] = int(applFields["user_id"])
            except:
                response["message"] = "Request has incorrect parameter type"
                status = 400
                return jsonify(response), status

            #Update application
            application.restName = applFields["restName"]
            application.user_id = applFields["user_id"]
            application.vendorType = applFields["vendorType"]
            application.reason = applFields["reason"]
            application.busLocation = applFields["busLocation"]
            models.db.session.commit()
            
            #Query Successful
            response["message"] = "Application successfully updated"
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "Application cannot be found"
            status = 200

    return jsonify(response), status

def delete(params):
    #Initialize
    response = {}
    requiredFields = ["id"]
    optionalFields = []
    allFields = requiredFields + optionalFields
    applFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        applFields[field] = params.get(field, None)
        
    #Check for Optional Fields
    for field in optionalFields:
        applFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Query for Product
        application = models.Application.query.filter_by(id=applFields["id"]).first()
        
        if application is not None:
            #Query Successful
            models.db.session.delete(application)
            models.db.session.commit()
            response["message"] = "Application successfully removed"
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "Application cannot be found"
            status = 200

    return jsonify(response), status