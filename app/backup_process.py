from  database import Database
from bson.objectid import ObjectId
import boto3
import subprocess
import crypto_bkfplus
import json
from utils_bkfplus import get_backup_file_or_directory_name
import time

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

database_engine_and_backup_script = {
    "mysql": "mysql.sh",
    "mongodb": "mongodb.sh",
    "postgresql": "postgresql.sh"
}




def start_log_backup_to_queue_process():
    # set the time interval (in seconds) to check for backup
    backup_interval = 86400

    while True:

        all_jobs = db.jobs.find({})

        for job in all_jobs:

            job["_id"] = str(job["_id"])
            backup_interval = int(job['interval_value'])

            # check if it's time to perform backup
            if int(time.time()) % backup_interval == 0:

                db.backup_queues.insert_one({
                    "_id": str(job['_id']),
                    "locked": False,
                    "job": job
                })

        # sleep for 1 second before checking again
        time.sleep(5)





def start_backup_process():
    while True:

        backup_queues = db.backup_queues.find({"locked": False}).limit(1)
        for backup in backup_queues:

            # Locked backup
            db.backup_queues.update_one({"_id": backup["_id"]}, {"$set": {"locked": True}})

            job = backup["job"]

            credential_object = db.manage_credentials.find_one({"_id": job["database_credential_id"]})
            credential_object = format_read_manage_credential_data(credential_object)

            credential = credential_object["credential"]

            database_engine = job["database_engine"]
            engine = database_engine["engine_or_storage_provider"]

            # directory to backup 
            # database to
            destination= "/var/backupforceplus/backup/"            

            filename_or_directory = get_backup_file_or_directory_name(credential['database_name'])
            script_path = f"{BASE_DIR}/db_backup_script/{database_engine_and_backup_script[engine['_id']]}"
            result = subprocess.run([
                script_path,
                credential['database_name'],
                credential['database_host'],
                credential['database_user'],
                credential['database_password'],
                destination,
                filename_or_directory
                ], stdout=subprocess.PIPE, shell=True)

            output = result.stdout.decode("utf-8")

            print(output)
        


        # sleep for 5 second before checking again
        time.sleep(5)



def format_read_manage_credential_data(data):
    try:

        # Decrypt data
        credential_decrypted = crypto_bkfplus.decrypt(str(data["credential"]).encode())

        data["credential"] = json.loads(credential_decrypted)
        return data

    except Exception as err:
        print(err)



if __name__ == "__main__":
    start_log_backup_to_queue_process()
        
