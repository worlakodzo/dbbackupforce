from functools import wraps
import os
import sys
import uuid
from datetime import datetime
from flask import Flask, render_template, redirect, session, request, jsonify, abort,url_for
from  database import Database
import logging
from prometheus_client import Counter, Histogram, Summary, generate_latest, Gauge,REGISTRY, Gauge, MetricsHandler, Info, make_wsgi_app 



from models import (
    create_db,
    Asset,
    User,

    STATUS_LIST,
    CATEGORY_LIST,
    )


error_msg = ""



UPLOAD_FOLDER =  os.path.join('static', 'vol/media/img')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# # Configure the logging
# logging.basicConfig(filename='app.log', level=logging.INFO)



# create flask application
app = Flask(__name__)


# Create a counter to track the number of requests to the endpoint
requests_total = Counter('requests_total', 'Total number of requests', ['method', 'endpoint'])
requests_count = Counter("request_count", "Number of requests to the endpoint")

#request_latency = Summary('request_latency_seconds', 'The latency of the request')

# Create a summary to track the request processing time
request_process_time = Summary("request_process_time_seconds", "Request processing time in seconds")

# Create a histogram to track the request latencies
request_latency = Histogram("request_latency_seconds", "Request latency in seconds")

# Create summary metric for response time of endpoint requests
response_time = Summary("request_response_time_seconds", "Time spent serving this endpoint")

# Create a counter metric for number of requests to endpoint
request_counter = Counter("endpoint_requests", "Number of requests to this endpoint")

# Create histogram metric for request payload size
request_payload = Histogram("request_payload_size_bytes", "Payload size of the request in bytes")

# Create gauge metric for available disk space
disk_space = Gauge("disk_space_free_bytes", "Free disk space in bytes")

# Create info metric with app version and deployment environment
app_info = Info("app_info", "Information about the app")



# configure the file upload folder
# and application security setting
app.config['SECRET_KEY'] = 'I-will-change-the-Secret-Code-Later'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# setup database connection
db, client = [None, None]
try:
    # setup database connection
    db, client = Database.get_database_mongo()

    # Create all database
    # tables
    create_db()
except:
    pass



@app.route('/health')
def health():
    app_msg ="Runing"
    db_server_msg = "Runing" 
    try:
        requests_total.labels('GET', '/health').inc()

        # Check database server connection
        db, client = Database.get_database_mongo()
        collections = db.list_collections()
    except:
        db_server_msg = "Not Runing"
    
    return jsonify({
        "application_server_status": app_msg,
        "database_server_status": db_server_msg
    })



def upload_img(file):

    file_path = ""
    actual_filename = ""
    new_filename = ""
    try:

        # Get file extension
        file_extension = file.filename.split(".")[1].lower().strip()


        # Get storage path
        root_path = UPLOAD_FOLDER

        actual_filename = file.filename

        # Build file path
        root_path = root_path.replace("\\", "/")
        new_filename = build_file_name(file_extension, "img")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)

        # Save file
        file.save(file_path)


        # PERMIT READ FILE
        try:
            os.chmod(file_path, 0o777)
        except Exception as e:
            print(str(e))
        # END PERMIT READ FILE


    except Exception as e:
        print(str(e))
        return {
                "filename": "blank-img.jpg",
                "actual_filename": "blank-img.jpg",
            }

    else:
        return {
                "filename": new_filename,
                "actual_filename": actual_filename,
            }


def build_file_name(file_extension, prefix):
    new_filename = f'{prefix}_{uuid.uuid4()}_{datetime.now().strftime("%d%m%y%I%M%S")}.{file_extension}'
    new_filename = new_filename.replace("-", "_")
    return new_filename

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)


# Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/login')

    return wrap


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'logged_in' in session:
        return redirect('/')

    if request.method == 'POST':

        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # Retrive user
        user = db.users.find_one({"username": username})

        try:
            # verify user account 
            if user and User.verify_user(user, password):

                # check if user
                # has permission to login
                if user["is_active"]:
                    # give user access
                    session['logged_in'] = True


                    del user['password']
                    session['user'] = user
                    return redirect('/')

                else:
                    # prompt user to contact adminstractor
                    error_message = """<p class="text-danger">Contact adminstractor for login access</p>"""
                    return render_template('login.html', error_message=error_message)


            else:
                # prompt user for login error
                error_message = """<p class="text-danger">Wrong Password or username</p>"""
                return render_template('login.html', error_message=error_message)

        except:
            for error in sys.exc_info():
                print("Oops!", error, "occurred.")
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route("/", methods=["GET", "POST"])
@login_required
def dashboard():

    today = datetime.now()

    total_asset_count = 0 # Asset.query.count()
    total_license_count = 0 # License.query.filter(License.expiration_date > today).count()


    total_asset_in_repair_count = 0 # License.query.filter(License.expiration_date >= today).count()
    number_of_license_due_expiry_count = 0 # License.query.filter(License.expiration_date <= today).count()


    return render_template(
        "index.html",
        total_asset_count = total_asset_count,
        total_license_count = total_license_count,
        number_of_license_due_expiry_count = number_of_license_due_expiry_count,
        total_asset_in_repair_count = total_asset_in_repair_count,
        is_dashboard=True
        )



@app.route('/user-list')
def users_list():
    return render_template("user-list.html", is_user=True)

@app.route('/user-profile/<string:user_id>')
def user_profile(user_id:str):
    return render_template("users-profile.html", user_id = user_id, is_user=True)

@app.route('/user_add')
def create_user():
    try:
        return render_template("users-add.html", is_user=True)    

    # The code below will 
    # execute when error occur
    # in the try block
    except Exception as err:
        # print out err to 
        # console for debug purpose
        print(str(err))

        # call to error handler
        abort(500)


@app.route("/assets", methods=["GET"])
def asset_list():
    try:
        # Retrieve all asset from database
        asset_query = Asset.query.all()
        assets = []

        # loop over all asset object 
        # and format the data
        for asset in asset_query:
            data = asset.format()

            # get link of asset image
            photo_link = os.path.join(app.config['UPLOAD_FOLDER'], asset.photo)
            data['photo_link'] = f"/{photo_link}"


            # add data to list of asset
            assets.append(data)

        return render_template("asset_list.html", assets= assets)

    # The code below will 
    # execute when error occur
    # in the try block
    except Exception as err:
        # print out err to 
        # console for debug purpose
        print(str(err))

        # call to error handler
        abort(500)

@app.route("/asset_add", methods=["GET", "POST"])
def asset_add():
    try:

        if request.method == "GET":
            return render_template("asset_add.html", status_list= STATUS_LIST)


        # get data submited from 
        # the frontend as dictionary object
        body = request.form
        photo = ""
        actual_photo_name = ""
        file_data = {}

        # save image
        default_image = "blank-img.jpg"
        if "upload_asset_image" in request.files:
            file = request.files['upload_asset_image']
            file_data = upload_img(file)

        # set default image
        # if image if not uploaded
        if file_data:
            photo= file_data['filename']
            actual_photo_name = file_data['actual_filename']
        else:
            photo= default_image
            actual_photo_name = default_image

        print("working")
        # Create new asset object
        asset = Asset(
            company= body["company"],
            asset_name= body["asset_name"],
            tags= body["asset_tag"],
            serial_number= body["asset_serial"],
            model= body["asset_model"],
            status= body["asset_status"],
            purchase_date= datetime.fromisoformat(body["purchase_date"]),
            supplier= body["supplier"],
            order_number= body["order_number"],
            purchase_cost= body["purchase_cost"],
            warranty= body["warranty"],
            note= body["note"],
            default_location= body["default_location"],
            photo= photo,
            actual_photo_name = actual_photo_name
            )

        # insert the new asset
        # into the database
        asset.insert()

        # return json data
        return jsonify({
            "success": True
        }), 201
    

    # The code below will 
    # execute when error occur
    # in the try block
    except Exception as err:
        # print out err to 
        # console for debug purpose
        print(str(err))

        # call to error handler
        abort(500)

@app.route("/asset_edit/<int:asset_id>", methods=["GET", "POST"])
def asset_edit(asset_id):
    try:

        if request.method == "GET":
            return render_template(
                "asset_edit.html",
                asset_id=asset_id,
                status_list= STATUS_LIST)


        # get data submited from 
        # the frontend as dictionary object
        body = request.form

        # save image
        file_data = {}
        if "upload_asset_image" in request.files:
            file = request.files['upload_asset_image']
            file_data = upload_img(file)

        # Get asset
        asset = Asset.query.get(asset_id)

        # update asset object
        asset.company= body["company"]
        asset.asset_name= body["asset_name"]
        asset.tags= body["asset_tag"]
        asset.serial_number= body["asset_serial"]
        asset.model= body["asset_model"]
        asset.status= body["asset_status"]
        asset.purchase_date= datetime.fromisoformat(body["purchase_date"])
        asset.supplier= body["supplier"]
        asset.order_number= body["order_number"]
        asset.purchase_cost= body["purchase_cost"]
        asset.warranty= body["warranty"]
        asset.note= body["note"]
        asset.default_location= body["default_location"]

        # update photo attribute
        # when new asset image is
        # loaded
        if file_data:
            if "filename" in file_data:
                asset.photo= file_data['filename']
                asset.actual_photo_name = file_data['actual_filename']
        

        # commit asset
        # into the database
        asset.update()

        # return json data
        return jsonify({
            "success": True
        }), 200
    

    # The code below will 
    # execute when error occur
    # in the try block
    except Exception as err:
        # print out err to 
        # console for debug purpose
        print(str(err))

        # call to error handler
        abort(500)




################## BEGIN API ###################################

@app.route('/users', methods=["GET", "POST"])
@request_latency.time()
@request_process_time.time()
def users():
    status_code = 500
    try:

        if request.method == "GET":
            requests_count.labels('GET', '/users').inc()
            requests_total.labels('GET', '/users').inc()

            # Retrieve all user from database
            user_query = db.users.find({})

            # loop over all user object 
            # and format the data
            users = [user for user in list(user_query)]
            return jsonify({
                "success": True,
                "data": users
            })

        elif request.method == "POST":
            requests_count.labels('POST', '/users').inc()
            requests_total.labels('POST', '/users').inc()

            body = request.get_json()
            print(body)
            new_user = User(**body)

            result = new_user.insert()

            return jsonify({
                "success": True,
                "_id": result.inserted_id
            })


    # The code below will 
    # execute when error occur
    # in the try block
    except Exception as err:
        # print out err to 
        # console for debug purpose
        print(str(err))

        # call to error handler
        abort(status_code)


@app.route('/users/<string:id>', methods=["GET", "PUT", "PATCH", "DELETE"])
def user_detail(id:str):
    '''
        Retrieve, update, and delete user profile
    '''
    status_code = 500
    try:

        if request.method == "GET":

            # Retrieve user from database
            user_query = db.users.find_one({"_id": id})

            # get link of user image
            photo_link = os.path.join(app.config['UPLOAD_FOLDER'], user_query['photo']['path'])
            user_query['photo_link'] = f"/{photo_link}"

            return jsonify({
                "success": True,
                "data": user_query
            }), 200


        elif request.method == "PUT":

            # Retrieve user from database
            user_query = db.users.find_one({"_id": id})
            body = request.get_json()

            if body["action_type"] == "update-user-data":

                return jsonify({
                    "success": True,
                    "data": update_user_data(body, user_query)
                }), 200


            elif body["action_type"] == "update-user-setting":

                return jsonify({
                    "success": True,
                    "data": update_user_setting(body, user_query)
                }), 200




        elif request.method == "PATCH":
            # Change password

            # Retrieve user from database
            user_query = db.users.find_one({"_id": id})
            body = request.get_json()

            reset_password(body, user_query)
            return jsonify({
                "success": True,
                "_id": id
            }), 200



        elif request.method == "DELETE":
            # delete user profile 
            user_query = db.users.delete_one({"_id": id})

            return jsonify({
                "success": True,
                "_id": id
            }), 204            
            



    # The code below will 
    # execute when error occur
    # in the try block
    except Exception as err:
        error_msg = str(err)
        # print out err to 
        # console for debug purpose
        print(str(err))

        # call to error handler
        abort(status_code)


def reset_password(body, user_query):
    new_value = {
        "password": User.get_hashed_password(body["password"]),
    }
    db.users.update_one({"_id": user_query["_id"]}, {"$set": new_value})



def update_user_data(body, user_query):

    new_value = {
        "full_name": body["full_name"],
        "about": body["about"],
        "job_title": body["job_title"],
        "address": body["address"],
        "phone": body["phone"],
        "email": body["email"],
        "photo": {
            "storage_type": user_query['photo']["storage_type"],
            "path": user_query["photo"]['path']
        },
        "social_link": {
            "twitter": body["twitter_link"],
            "facebook": body["facebook_link"],
            "linkedin": body["linkedin_link"]
        }
    }

    db.users.update_one({"_id": user_query["_id"]}, {"$set": new_value})

    # Get new record and return new record
    return db.users.find_one({"_id": user_query["_id"]})

def update_user_setting(body, user_query):

    new_value = {
        "email_notification": {
            "changes_made_to_account": body["changes_made_to_account"],
            "new_assert_added": body["new_assert_added"],
            "assert_expiring": body["assert_expiring"],
            "security_notify": body["security_notify"]
        }
    }

    db.users.update_one({"_id": user_query["_id"]}, {"$set": new_value})

    # Get new record and return new record
    return db.users.find_one({"_id": user_query["_id"]})




# user = db.users.find_one({"username":"admin"})
# reset_password({"password": "admin"}, user)
################  END API ##########################################




# Add a gauge metric for available disk space
@app.route("/diskspace")
def disk_space_handler():
    # Set the gauge metric value
    disk_space.set(1024 * 1024 * 1024)
    return "Disk Space: 1 GB"

# Add a info metric with app version and deployment environment
app_info.info({"version": "1.0.1", "environment": "development"})

# # Expose the metrics on /metrics endpoint
# app.add_url_rule("/metrics", "metrics", MetricsHandler.as_view(registry=app.registry))
@app.route('/metrics')
def metrics():
    return generate_latest()




"""
Error handle
"""

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
    }), 500


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method Not Allowed"
    }), 405

@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": f"Resource Not Found {error_msg}"
    }), 404

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401


# UASSET 
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)