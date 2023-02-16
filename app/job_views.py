from flask import Blueprint
from flask import Flask, render_template, redirect, session, request, jsonify, abort,url_for
job = Blueprint('job', __name__)



@job.route('/job_list')
def job_list():
    return render_template("job-list.html", is_jobs=True)


@job.route('/job_add')
def job_add():
    return render_template("jobs-create-and-update.html", page_title= "Add")

@job.route('/job_edit')
def job_edit():
    return render_template("jobs-create-and-update.html", page_title= "Edit")




###### API ######################

@job.route('/jobs', methods = ["GET", "POST"])
def jobs():
    pass


@job.route('/jobs/<string:job_id>', methods = ["GET", "POST", "PUT", "PATCH", "DELETE"])
def job_details(job_id:str):
    pass