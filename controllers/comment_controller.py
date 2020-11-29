from flask import jsonify
from models import models
from controllers import base_controller
import time, datetime

def create(params): 
    #Initialize
    response = {}
    requiredFields = ["post_id", "user_id", "com_info"]
    optionalFields = []
    allFields = requiredFields + optionalFields
    commentFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        commentFields[field] = params.get(field, None)
        
    #Check for Optional Fields
    # for field in optionalFields:
    #     if field == "frequency":
    #         applFields[field] = params.get(field, 0)
    #     else:
    #         applFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Check for Numerical Price and Frequency
        try:
            commentFields["post_id"] = int(commentFields["post_id"])
            commentFields["user_id"] = int(commentFields["user_id"])
        except:
            response["message"] = "Request has incorrect parameter type"
            status = 400
            return jsonify(response), status

        #Check for Valid Vendor Type
        # if commentFields["vendorType"] not in ["Home", "Business"]:
        #     response["message"] = "vendorType must be either Home or Business"
        #     status = 400
        #     return jsonify(response), status

        #Add Product to Database
        comment = models.Comment(
            post_id=commentFields["post_id"],
            user_id=commentFields["user_id"],
            com_info=commentFields["com_info"],
            com_date=datetime.date.today()
            )
        models.db.session.add(comment)
        models.db.session.commit()
        response["message"] = "Comment created successfully!"
        status = 200
  
    return jsonify(response), status

def show(params):
    #Initialize
    response = {}
    requiredFields = ["id"]
    optionalFields = []
    allFields = requiredFields + optionalFields
    commentFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        commentFields[field] = params.get(field, None)
        
    #Check for Optional Fields
    for field in optionalFields:
        commentFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Query for Comment
        comment = models.Comment.query.filter_by(id=commentFields["id"]).first()
        
        if comment is not None:
            #Query Successful
            response["id"] = comment.id
            response["post_id"] = comment.post_id
            response["user_id"] = comment.user_id
            response["com_date"] = str(comment.com_date)
            response["com_info"] = comment.com_info
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "Comment cannot be found"
            status = 200

    return jsonify(response), status

def display_all(params):
    comments = models.Comment.query.all()
    response = {}
    for comment in comments:
        response[comment.id] = {
            "comment_id" : comment.id,
            "post_id": comment.post_id,
            "user_id": comment.user_id,
            "com_date": str(comment.com_date),
        }
    status = 200
    return jsonify(response), status

# def update(params):
#     #Initialize
#     response = {}
#     requiredFields = ["id", "user_id", "restName", "vendorType", "reason"]
#     optionalFields = ["busLocation"]
#     allFields = requiredFields + optionalFields
#     applFields = {}

#     #Check for Required Fields
#     for field in requiredFields:
#         if params.get(field, None) == None:
#             response["message"] = "Missing Required Parameters: {}".format(requiredFields)
#             status = 400
#             return jsonify(response), status
#         applFields[field] = params.get(field, None)

#     #Check for Optional Fields
#         for field in optionalFields:
#             applFields[field] = params.get(field, None)

#     #Check for Invalid Parameters
#     if base_controller.verify(params, allFields): 
#         response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
#         status = 400
#     else:
#         #Query for Product
#         application = models.Application.query.filter_by(id=applFields["id"]).first()     

#         if application is not None:
#             #Check for Numerical Price and Frequency
#             try:
#                 applFields["user_id"] = int(applFields["user_id"])
#             except:
#                 response["message"] = "Request has incorrect parameter type"
#                 status = 400
#                 return jsonify(response), status

#             #Update application
#             application.restName = applFields["restName"]
#             application.user_id = applFields["user_id"]
#             application.vendorType = applFields["vendorType"]
#             application.reason = applFields["reason"]
#             application.busLocation = applFields["busLocation"]
#             models.db.session.commit()
            
#             #Query Successful
#             response["message"] = "Application successfully updated"
#             status = 200
#         else:
#             #Query Unsuccessful
#             response["message"] = "Application cannot be found"
#             status = 200

#     return jsonify(response), status

def delete(params):
    #Initialize
    response = {}
    requiredFields = ["id"]
    optionalFields = []
    allFields = requiredFields + optionalFields
    commentFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        commentFields[field] = params.get(field, None)
        
    #Check for Optional Fields
    for field in optionalFields:
        commentFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, allFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, allFields))
        status = 400
    else:
        #Query for comment
        comment = models.Comment.query.filter_by(id=commentFields["id"]).first()
        
        if comment is not None:
            #Query Successful
            models.db.session.delete(comment)
            models.db.session.commit()
            response["message"] = "Comment successfully removed"
            status = 200
        else:
            #Query Unsuccessful
            response["message"] = "Comment cannot be found"
            status = 200

    return jsonify(response), status