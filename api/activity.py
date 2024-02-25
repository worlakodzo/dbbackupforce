from  database import Database
from bson.objectid import ObjectId

# pip install boto3
# setup database connection
db, client = [None, None]
try:
    # setup database connection
    db, client = Database.get_database_mongo()
except Exception as err:
    print(err)


data = {
    "content": "",
    "log_type": "",
    "reference_id": "",
    "log_datetime": ""
}

def log_activity(data):
    db.activity_logs.insert_one(data)
