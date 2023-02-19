import os
from flask import Blueprint
from flask import render_template, request, jsonify, abort
from  database import Database
from bson.objectid import ObjectId
job = Blueprint('job', __name__)


# setup database connection
db, client = [None, None]
try:
    # setup database connection
    db, client = Database.get_database_mongo()
except Exception as err:
    print(err)



@job.route('/job_list')
def job_list():
    return render_template("job-list.html", is_jobs=True)


@job.route('/job_add')
def job_add():
    return render_template("jobs-create-and-update.html", action_type= "Add", method = "POST")

@job.route('/job_edit/<string:job_id>')
def job_edit(job_id:str):
    return render_template("jobs-create-and-update.html", job_id= job_id, action_type= "Edit" , method = "PUT")




###### API ######################

@job.route('/jobs', methods = ["GET", "POST"])
def jobs():
    status_code = 500
    try:

        if request.method == "GET":

            # Get jobs
            jobs_query = db.jobs.find({})

            return jsonify({
                "success": True,
                "jobs": [format_read_job_data(job) for job in jobs_query],
            })
        


        elif request.method == "POST":
            body = request.get_json()

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



@job.route('/jobs/<string:job_id>', methods = ["GET", "POST", "PUT", "DELETE"])
def job_details(job_id:str):
    status_code = 500
    try:

        if request.method == "GET":

            # Get job
            job = db.jobs.find_one({"_id": ObjectId(job_id)})

            if job:
                job = format_read_job_data(job)

            else:
                status_code = 404
                os.environ['error_msg'] = f"Job with id {job_id} does not exist."
                abort(404)

            return jsonify({
                "success": True,
                "job": job
            })



        elif request.method == "PUT":

            body = request.get_json()
            # body = format_read_job_data(body)

            # Save data
            res = db.jobs.update_one({"_id": ObjectId(job_id)}, {"$set": body})

            # Retrieve data
            job = db.jobs.find_one({"_id": ObjectId(job_id)})

            return jsonify({
                "success": True,
                "job": format_read_job_data(job)
            })



        elif request.method == "DELETE":

            # Get job
            job = db.jobs.find_one({"_id": ObjectId(job_id)})

            if job:
                # Delete document
                db.jobs.delete_one({"_id": ObjectId(job_id)})

            else:
                status_code = 404
                os.environ['error_msg'] = f"Job with id {job_id} does not exist."
                abort(404)

            return jsonify({
                "success": True,
                "job_id": job_id
            })



        else:
            status_code = 400
            abort(400)            


    except Exception as err:
        print(str(err))
        abort(status_code)



def format_read_job_data(data):

    try:

        data["_id"] = str(data["_id"])
        return data
    except Exception as err:
        print(err)
        abort(500)



@job.route('/jobbasicinfo')
def job_basic_info():
    status_code = 500
    try:

        # Get manage credentials
        credentials_query = db.manage_credentials.find({}, {"credential": 0} )
        credentials = [data for data in credentials_query]

        # Get duration interval
        duration_intervals_query = db.job_duration_interval_types.find({})

        return jsonify({
            "success": True,
            "credentials": credentials,
            "duration_interval_types": list(duration_intervals_query)
        })
      


    except Exception as err:
        print(str(err))
        abort(status_code)





"""
Error handle
"""

@job.errorhandler(500)
def internal_server_error(error):
    error_msg = os.environ.get("error_msg", "")
    return jsonify({
        "success": False,
        "error": 500,
        "message": f"Internal Server Error, {error_msg}"
    }), 500


@job.errorhandler(405)
def method_not_allowed(error):
    error_msg = os.environ.get("error_msg", "")
    return jsonify({
        "success": False,
        "error": 405,
        "message": f"Method Not Allowed, {error_msg}"
    }), 405

@job.errorhandler(404)
def resource_not_found(error):
    error_msg = os.environ.get("error_msg", "")
    return jsonify({
        "success": False,
        "error": 404,
        "message": f"Resource Not Found, {error_msg}"
    }), 404
