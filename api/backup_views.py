import os
from flask import Blueprint
from flask import render_template, request, jsonify, abort
from  database import Database
from bson.objectid import ObjectId
import boto3
import subprocess
from utils_bkfplus import get_backup_file_or_directory_name
import time
backup = Blueprint('backup', __name__)
from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# pip install boto3
# setup database connection
db, client = [None, None]
try:
    # setup database connection
    db, client = Database.get_database_mongo()
except Exception as err:
    print(err)



@backup.route('/backup_list')
def get_backups_overview():
    return render_template("job-backup-detail.html", is_backup=True)

@backup.route('/backup_list/<string:job_id>')
def get_backup_overview(job_id:str):
    return render_template("job-backup-detail.html", is_jobs=True, job_id=job_id)



###### API ######################

@backup.route('/backups', methods = ["GET", "POST"])
def backups():
    status_code = 500
    try:

        if request.method == "GET":

            # Get jobs
            backups_query = db.backup_histories.find({})

            return jsonify({
                "success": True,
                "backup_histories": [format_read_job_data(backup) for backup in backups_query],
            })
        


        elif request.method == "POST":
            body = request.get_json()

            # Retrieve data
            engine_res = db.manage_credentials.find_one({"_id": body["database_credential_id"]}, {"credential": 0})
            provider_res = db.manage_credentials.find_one({"_id": body["backup_storage_provider_credential_id"]}, {"credential": 0})


            body['database_engine'] = engine_res
            body['storage_provider'] = provider_res


            # Save data
            res = db.jobs.insert_one(body)


            # Retrieve data
            job = db.jobs.find_one({"_id": res.inserted_id})

            return jsonify({
                "success": True,
                "job": format_read_job_data(job)
            }), 201

        else:
            status_code = 405
            abort(405)            


    except Exception as err:
        print(str(err))
        abort(status_code)



@backup.route('/backups/<string:job_id>/histories')
def backup_histories(job_id:str):
    status_code = 500
    try:

        # Get backup history
        backups_query = db.backup_histories.find({"job._id": ObjectId(job_id)})

        return jsonify({
            "success": True,
            "backup_histories": [format_read_job_data(backup) for backup in backups_query],
        })


    except Exception as err:
        print(str(err))
        abort(status_code)





def format_read_job_data(data):

    try:

        job = data["job"]
        data["_id"] = str(data["_id"])
        job["_id"] = str(job["_id"])

        data["job"] = job

        return data
    except Exception as err:
        print(err)
        abort(500)



def run_backup(script_name):
    script_path = f"/path/to/{script_name}"
    result = subprocess.run([script_path, "arg1", "arg2"], stdout=subprocess.PIPE, shell=True)
    output = result.stdout.decode("utf-8")
    return True



def upload_backup_to_aws_s3(
    aws_access_key_id,
    aws_secret_access_key,
    bucket_name,
    file_name,
    file_path
    ):

    s3_key = file_name

    # Create an S3 client
    s3_client = boto3.client('s3',
                            aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)

    # Upload the file to S3
    s3_client.upload_file(file_path, bucket_name, s3_key)

    log = f'{file_name} uploaded to {bucket_name} with key {s3_key}.'

    print(log)
    return True




"""
Error handle
"""

@backup.errorhandler(500)
def internal_server_error(error):
    error_msg = os.environ.get("error_msg", "")
    return jsonify({
        "success": False,
        "error": 500,
        "message": f"Internal Server Error, {error_msg}"
    }), 500


@backup.errorhandler(405)
def method_not_allowed(error):
    error_msg = os.environ.get("error_msg", "")
    return jsonify({
        "success": False,
        "error": 405,
        "message": f"Method Not Allowed, {error_msg}"
    }), 405

@backup.errorhandler(404)
def resource_not_found(error):
    error_msg = os.environ.get("error_msg", "")
    return jsonify({
        "success": False,
        "error": 404,
        "message": f"Resource Not Found, {error_msg}"
    }), 404

