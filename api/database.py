import os
from flask import abort

class Database:

    @staticmethod
    def get_database_mongo():
        # Get connection host and port
        db_name = os.environ.get("PORTFOLIO_MONGO_DB_NAME")
        CONNECTION_STRING = os.environ.get("PORTFOLIO_MONGO_DB_URI")


        try:
            from pymongo import MongoClient
            # Connect to database
            client = MongoClient(CONNECTION_STRING)
            return client[db_name], client

        # The code below excute
        # When error occur when
        # connecting to database
        except Exception as e:
            print(f"{e}")
            abort(500)



if __name__ == "__main__":
    db, client = Database.get_database_mongo()
