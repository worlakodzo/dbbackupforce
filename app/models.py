from database import Database
import uuid

db, _ = Database.get_database_mongo()

def create_db():

    # retrieve user
    user = db.users.find_one({"username":"sysadmin"})

    # create default if it
    # does not exist
    if not user:
        # Create a default user
        user = User(
            username= "sysadmin",
            password= "admin",
            phone= "0245000001",
            email= "admin@uasset.com",
            full_name= "Admin",
            is_active= True,
            is_admin= True
        )

        # insert the default user
        # into database
        
        user.insert()


class User():

    # Constructor
    def __init__(
        self,
        username,
        full_name,
        password,
        phone,
        email,
        photo="default.png",
        photo_storage_type="local",
        _id= "",
        about= "",
        job_title= "",
        address= "",
        twitter_link= "",
        facebook_link= "",
        linkedin_link= "",
        changes_made_to_account= False,
        new_assert_added= False,
        assert_expiring= False,
        security_notify= False,
        is_active= True,
        is_admin= False,
        ):

        self.username = username
        self.password = password
        self.is_active = is_active
        self.is_admin = is_admin
        self.photo = photo
        self.photo_storage_type = photo_storage_type
        self._id = _id
        self.full_name = full_name
        self.about = about
        self.job_title = job_title
        self.address = address
        self.phone = phone
        self.email = email
        self.twitter_link = twitter_link
        self.facebook_link = facebook_link
        self.linkedin_link = linkedin_link
        self.changes_made_to_account = changes_made_to_account
        self.new_assert_added = new_assert_added
        self.assert_expiring = assert_expiring
        self.security_notify = security_notify


    
    def insert(self):

        # create new user
        result = db.users.insert_one({
            "_id": str(uuid.uuid4()),
            "username": self.username,
            "password": User.get_hashed_password(self.password),
            "is_active": self.is_active,
            "is_admin": self.is_admin,
            "full_name": self.full_name,
            "about": self.about,
            "job_title": self.job_title,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
            "photo": {
                "storage_type": self.photo_storage_type,
                "path": self.photo
            },
            "email_notification": {
                "changes_made_to_account": self.changes_made_to_account,
                "new_assert_added": self.new_assert_added,
                "assert_expiring": self.assert_expiring,
                "security_notify": self.security_notify
            },
            "social_link": {
                "twitter": self.twitter_link,
                "facebook": self.facebook_link,
                "linkedin": self.linkedin_link
            }
        })

        return result


    def update(self):
        # update existing user
        new_value = {
            "is_active": self.is_active,
            "is_admin": self.is_admin,
            "full_name": self.full_name,
            "about": self.about,
            "job_title": self.job_title,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
            "photo": {
                "storage_type": self.photo_storage_type,
                "path": self.photo
            },
            "email_notification": {
                "changes_made_to_account": self.changes_made_to_account,
                "new_assert_added": self.new_assert_added,
                "assert_expiring": self.assert_expiring,
                "security_notify": self.security_notify
            },
            "social_link": {
                "twitter": self.twitter_link,
                "facebook": self.facebook_link,
                "linkedin": self.linkedin_link
            }
        }

        db.users.update_one({"_id": self._id}, {"$set": new_value})
        return True

    
    @staticmethod
    def get_hashed_password(raw_password):
        # import hash library
        from hashlib import sha256

        # hash password and return hashed value
        return sha256(str(raw_password).encode('utf-8')).hexdigest()

    @staticmethod
    def verify_user(user, raw_password):

        new_hashed_password = User.get_hashed_password(raw_password)

        # return true if new-hashed password
        # is equal to user hashed password in database
        if user["password"] == new_hashed_password:
            return True
        else:
            return False


    def format(self):
        # Json format
        # of the user data
        return {
            "user_id": self._id,
            "username": self.username,
            "is_active": self.is_active,
            "is_admin": self.is_admin
            }




