import json
from flask import Blueprint
from flask import Flask, render_template, redirect, session, request, jsonify, abort,url_for
from  database import Database
import crypto_bkfplus
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
            credentials = [format_read_manage_credential_data(data) for data in list(credentials_query)]

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

            # Save data
            res = db.manage_credentials.insert_one(body)

            # Retrieve data
            credential = db.manage_credentials.find_one({"_id": res.inserted_id})

            return jsonify({
                "success": True,
                "credential": format_read_manage_credential_data(credential)
            }), 201

        else:
            status_code = 400
            abort(400)            


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
                status_code = 400
                abort(400)

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
                status_code = 400
                abort(400)

            return jsonify({
                "success": True,
                "credential_id": credential_id
            })



        else:
            status_code = 400
            abort(400)            


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
