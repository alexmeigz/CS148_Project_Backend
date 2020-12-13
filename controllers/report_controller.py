from flask import jsonify
from models import models
from controllers import base_controller
import time, datetime
from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash


def create(params, body): 
    #Initialize
    response = {}
    requiredFields = ["userReporter_id", "reportedUser_id"]
    optionalFields = []
    allFields = requiredFields + optionalFields
    reportFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        reportFields[field] = params.get(field, None)
        
    #Check for Optional Fields
    for field in optionalFields:
        if field == "frequency":
            reportFields[field] = params.get(field, 0)
        else:
            reportFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400

    
    else:
        #Check for nonempty body
        if body.decode().strip() == "":
            response["message"] = "Report content cannot be null"
            status = 400
            return jsonify(response), status

        #Add Report to Database
        report = models.Report(
            userReporter_id=reportFields["userReporter_id"],
            reportedUser_id=reportFields["reportedUser_id"],
            reportText=body.decode(),
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
    reportFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        reportFields[field] = params.get(field, None)
        
    #Check for Optional Fields
    for field in optionalFields:
        reportFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Query for Report
        report = models.Report.query.filter_by(report_id=reportFields["report_id"]).first()
        
        if report is not None:
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


def display_all(params):
    reports = models.Report.query.all()
    response = {}
    for report in reports:
        response[report.report_id] = {
            "reportDate": str(report.reportDate),
            "userReporter_id": report.userReporter_id,
            "reportedUser_id": report.reportedUser_id,
            "report_id" : report.report_id,
            "reportText": report.reportText
        }
    status = 200
    return jsonify(response), status

def update(params, body):
    #Initialize
    response = {}
    requiredFields = ["report_id"]
    optionalFields = []
    allFields = requiredFields + optionalFields
    reportFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        reportFields[field] = params.get(field, None)

    #Check for Optional Fields
        for field in optionalFields:
            reportFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Query for Report
        report = models.Report.query.filter_by(report_id=reportFields["report_id"]).first()     

        if report is not None:
            ''''#Check for Numerical Price and Frequency
            try:
                applFields["user_id"] = int(applFields["user_id"])
            except:
                response["message"] = "Request has incorrect parameter type"
                status = 400
                return jsonify(response), status'''

            #Update report
            report.reportText = body.decode()
            models.db.session.commit()
            
            #Query Successful
            response["message"] = "Report successfully updated. Please refresh the screen to see updates."
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "Report cannot be found"
            status = 200

    return jsonify(response), status

def delete(params):
    #Initialize
    response = {}
    requiredFields = ["report_id"]
    optionalFields = []
    allFields = requiredFields + optionalFields
    reportFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        reportFields[field] = params.get(field, None)
        
    #Check for Optional Fields
    for field in optionalFields:
        reportFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Query for Report
        report = models.Report.query.filter_by(report_id=reportFields["report_id"]).first()
        
        if report is not None:
            #Query Successful
            models.db.session.delete(report)
            models.db.session.commit()
            response["message"] = "Report successfully removed. Please refresh the screen to see updates."
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "Report cannot be found"
            status = 200

    return jsonify(response), status

def delete_all(params):
    #Initialize
    response = {}
    requiredFields = ["userReporter_id"]
    optionalFields = []
    allFields = requiredFields + optionalFields
    reportFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(field)
            status = 400
            return jsonify(response), status
        reportFields[field] = params.get(field, None)
        
    #Check for Optional Fields
    for field in optionalFields:
        reportFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Query for report
        report = models.Report.query.filter_by(userReporter_id=reportFields["userReporter_id"]).first()
        while(report is not None):
            #Query Successful
            models.db.session.delete(report)
            report = models.Report.query.filter_by(userReporter_id=reportFields["userReporter_id"]).first()

        models.db.session.commit()
        response["message"] = "Reports successfully removed"
        status = 200

    return jsonify(response), status