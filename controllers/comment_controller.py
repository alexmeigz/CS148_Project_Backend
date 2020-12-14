from flask import jsonify
from models import models
from controllers import base_controller, user_controller
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

        #Add Comment to Database
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
    #Initialize
    response = {}
    requiredFields = ["post_id", "display_all"]
    commentFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(requiredFields)
            status = 400
            return jsonify(response), status
        commentFields[field] = params.get(field, None)

    #Check for Invalid Parameters
    if base_controller.verify(params, requiredFields): 
        response["message"] = "Request has invalid parameter {}".format(base_controller.verify(params, requiredFields))
        status = 400
    else:
        #Query for Comment
        comments = models.Comment.query.filter_by(post_id=commentFields["post_id"]).all()

        for comment in comments:
            user = models.User.query.filter_by(user_id=comment.user_id).first()
            if user == None:
                response["message"] = "User for comment cannot be found"
                status = 400
                return jsonify(response), status

            response[comment.id] = {
                "comment_id" : comment.id,
                "com_info" : comment.com_info,
                "post_id": comment.post_id,
                "user_id": comment.user_id,
                "username": user.username,
                "com_date": str(comment.com_date)
            }

        status = 200
    return jsonify(response), status

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

def delete_all(params):
    #Initialize
    response = {}
    requiredFields = []
    optionalFields = ["post_id", "user_id"]
    allFields = requiredFields + optionalFields
    commentFields = {}

    #Check for Required Fields
    for field in requiredFields:
        if params.get(field, None) == None:
            response["message"] = "Missing Required Parameters: {}".format(field)
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
        #Query for comments
        if(commentFields.get("post_id") != None):
            comment = models.Comment.query.filter_by(post_id=commentFields["post_id"]).first()
            while(comment is not None):
                models.db.session.delete(comment)
                comment = models.Comment.query.filter_by(post_id=commentFields["post_id"]).first()
        elif(commentFields.get("user_id") != None):
            comment = models.Comment.query.filter_by(user_id=commentFields["user_id"]).first()
            while(comment is not None):
                models.db.session.delete(comment)
                comment = models.Comment.query.filter_by(user_id=commentFields["user_id"]).first()

        models.db.session.commit()
        response["message"] = "Comments successfully removed"
        status = 200

    return jsonify(response), status