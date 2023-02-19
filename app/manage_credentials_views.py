import json
from flask import Blueprint
from flask import render_template, request, jsonify, abort
from  database import Database
import crypto_bkfplus
import os
mcredential = Blueprint('mcredential', __name__)


# setup database connection
db, client = [None, None]
try:
    # setup database connection
    db, client = Database.get_database_mongo()
except Exception as err:
    print(err)




@mcredential.route('/credential_list')
def credential_list():
    return render_template("manage-credential-list.html", is_manage_credential=True)



###### API ######################

@mcredential.route('/credentials', methods = ["GET", "POST"])
def credentials():
    status_code = 500
    try:

        if request.method == "GET":

            # Get manage credentials
            credentials_query = db.manage_credentials.find({})
            credentials = [format_read_manage_credential_data(data) for data in credentials_query]

            # Get manage credential types
            credentials_types_query = db.manage_credential_types.find({})

            return jsonify({
                "success": True,
                "credentials": credentials,
                "credential_types": list(credentials_types_query)
            })
        
        elif request.method == "POST":
            body = request.get_json()
            body = format_save_manage_credential_data(body)

            # Get manage credential
            # check if id exist
            credential_old = db.manage_credentials.find_one({"_id": body["_id"]})
            print("worlako")
            if credential_old:

                os.environ['error_msg'] = f"Credential Indentifier ({body['_id']}) already exist."
                status_code = 500
                abort(500)

            # Save data
            res = db.manage_credentials.insert_one(body)
           
            # Retrieve data
            credential = db.manage_credentials.find_one({"_id": res.inserted_id})

            return jsonify({
                "success": True,
                "credential_data": format_read_manage_credential_data(credential)
            }), 201

        else:
            status_code = 405
            abort(405)            


    except Exception as err:
        print(str(err))
        abort(status_code)




@mcredential.route('/credentials/<string:credential_id>', methods = ["GET", "PUT", "DELETE"])
def credential_detail(credential_id:str):
    status_code = 500
    try:

        if request.method == "GET":

            # Get manage credential
            credential = db.manage_credentials.find_one({"_id": credential_id})

            if credential:
                credential = format_read_manage_credential_data(credential)

            else:
                status_code = 404
                os.environ['error_msg'] = f"Credential with id {credential_id} does not exist."
                abort(404)

            return jsonify({
                "success": True,
                "credential_data": credential
            })



        elif request.method == "PUT":

            body = request.get_json()
            body = format_save_manage_credential_data(body)

            # Save data
            res = db.manage_credentials.update_one({"_id": credential_id}, {"$set": body})

            # Retrieve data
            credential = db.manage_credentials.find_one({"_id": credential_id})

            return jsonify({
                "success": True,
                "credential_data": format_read_manage_credential_data(credential)
            })



        elif request.method == "DELETE":

            # Get manage credential
            credential = db.manage_credentials.find_one({"_id": credential_id})

            if credential:
                # Delete document
                db.manage_credentials.delete_one({"_id": credential_id})

            else:
                status_code = 404
                os.environ['error_msg'] = f"Credential with id {credential_id} does not exist."
                abort(404)

            return jsonify({
                "success": True,
                "credential_id": credential_id
            })



        else:
            status_code = 405
            abort(405)            


    except Exception as err:
        print(str(err))
        abort(status_code)



def format_read_manage_credential_data(data):
    try:

        # Decrypt data
        credential_decrypted = crypto_bkfplus.decrypt(str(data["credential"]).encode())

        data["credential"] = json.loads(credential_decrypted)
        return data

    except Exception as err:
        print(err)
        abort(500)
        


def format_save_manage_credential_data(data):

    try:

        credential_dumps = json.dumps(data["credential"])

        # Encrypt data
        data["credential"] = crypto_bkfplus.encrypt(credential_dumps).decode()
        return data
    except Exception as err:
        print(err)
        abort(500)





"""
Error handle
"""

@mcredential.errorhandler(500)
def internal_server_error(error):
    error_msg = os.environ.get("error_msg", "")
    return jsonify({
        "success": False,
        "error": 500,
        "message": f"Internal Server Error, {error_msg}"
    }), 500


@mcredential.errorhandler(405)
def method_not_allowed(error):
    error_msg = os.environ.get("error_msg", "")
    return jsonify({
        "success": False,
        "error": 405,
        "message": f"Method Not Allowed, {error_msg}"
    }), 405

@mcredential.errorhandler(404)
def resource_not_found(error):
    error_msg = os.environ.get("error_msg", "")
    return jsonify({
        "success": False,
        "error": 404,
        "message": f"Resource Not Found, {error_msg}"
    }), 404
