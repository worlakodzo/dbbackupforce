from flask import Blueprint
from flask import Flask, render_template, redirect, session, request, jsonify, abort,url_for
job = Blueprint('job', __name__)



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
    pass


@job.route('/jobs/<string:job_id>', methods = ["GET", "POST", "PUT", "PATCH", "DELETE"])
def job_details(job_id:str):
    pass