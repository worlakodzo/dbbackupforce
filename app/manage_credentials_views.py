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

        # Get manage credentials
        credentials_query = db.manage_credentials.find({})
        credentials = [format_read_manage_credential_data(data) for data in list(credentials_query)]

        # Get manage credential types
        credentials_types_query = db.manage_credential_types.find({})

    except:

        abort(status_code)

    else:

        return jsonify({
            "success": True,
            "credentials": credentials,
            "credential_types": list(credentials_types_query)
        })



def format_read_manage_credential_data(data):
    # Decrypt data
    credential_decrypted = crypto_bkfplus.decrypt(data["credential"])

    data["credential"] = json.loads(credential_decrypted)
    return data


def format_save_manage_credential_data(data):
    credential_dumps = json.dumps(data["credential"])

    # Encrypt data
    data["credential"] = crypto_bkfplus.encrypt(credential_dumps)
    return data




@mcredential.route('/credentials/<string:id>', methods = ["GET", "POST", "PUT", "PATCH", "DELETE"])
def credential_details(id:str):
    pass