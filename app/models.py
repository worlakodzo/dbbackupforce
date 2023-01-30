from database import Database
import uuid

# List of status
STATUS_LIST = [
    {
        "id":1,
        "name": "Archived"
    },
    {
        "id":2,
        "name": "Pending"
    },
    {
        "id":3,
        "name": "Ready to Deploy"
    }
]

# List of supplier
SUPPLIER_LIST = [
    {
        "id":1,
        "name": "Supplier 1"
    },
    {
        "id":2,
        "name": "Supplier 2"
    },
    {
        "id":3,
        "name": "Supplier 3"
    }
]

# List of companies
COMPANY_LIST = [
    {
        "id":1,
        "name": "Company 1"
    },
    {
        "id":2,
        "name": "Company 2"
    },
    {
        "id":3,
        "name": "Company 3"
    }
]

# List of category
CATEGORY_LIST = [
    {
        "id":1,
        "name": "Antivirus"
    },
    {
        "id":2,
        "name": "Misc Software"
    },
    {
        "id":3,
        "name": "Windows"
    },
    {
        "id":4,
        "name": "Linux"
    }
]

# List of manufacturer
MANUFACTURER_LIST = [
    {
        "id":1,
        "name": "Apache"
    },{
        "id":2,
        "name": "Apple Inc"
    }
]


db, _ = Database.get_database_mongo()

def create_db():

    # retrieve user
    user = db.users.find_one({"username":"admin"})

    # create default if it
    # does not exist
    if not user:
        # Create a default user
        user = User(
            username= "admin",
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



class Asset():
    # id = Column(Integer, primary_key = True)
    # company = Column(String(100), nullable= True, default = " ")
    # asset_name = Column(String(100), nullable= False)
    # tags = Column(String(50), nullable= False)
    # serial_number = Column(String(50), nullable= False)
    # model = Column(String(50), nullable= False)
    # status = Column(String(50), nullable= False)
    # purchase_date = Column(Date, nullable= False)
    # supplier = Column(String(100), nullable= True, default = " ")
    # order_number = Column(String(50), nullable= True, default = "")
    # purchase_cost = Column(Float, nullable= False)
    # warranty = Column(String(100), nullable= True, default =" ")
    # note = Column(String, nullable= True, default= " ")
    # default_location = Column(String, nullable= False)
    # photo = Column(String(255), nullable= True, default="")
    # actual_photo_name = Column(String(255), nullable= True, default= " ")
    # is_on_repair = Column(Boolean, default=False)

    # Constructor
    def __init__(
        self,
        company,
        asset_name,
        tags,
        serial_number,
        model,
        status,
        purchase_date,
        supplier,
        order_number,
        purchase_cost,
        warranty,
        default_location,
        photo = "blank-img.jpg",
        actual_photo_name = "blank-img.jpg",
        note = " ",
        ):

        self.company = company
        self.asset_name = asset_name
        self.tags = tags
        self.serial_number = serial_number
        self.model = model
        self.status = status
        self.purchase_date = purchase_date
        self.supplier = supplier
        self.order_number = order_number
        self.purchase_cost = purchase_cost
        self.warranty = warranty
        self.note = note
        self.photo = photo
        self.actual_photo_name = actual_photo_name
        self.default_location = default_location



    def insert(self):
        # create a new asset
        db.session.add(self)
        db.session.commit()

    def update(self):
        # update existing asset
        db.session.commit()


    def delete(self):
        # delete an asset
        db.session.delete(self)
        db.session.commit()


    def format(self):
        # json format of 
        # asset data
        return {
            "asset_id": self.id,
            "company": self.company,
            "asset_name": self.asset_name,
            "asset_tag": self.tags,
            "asset_serial": self.serial_number,
            "asset_model": self.model,
            "asset_status": self.status,
            "supplier": self.supplier,
            "order_number": self.order_number,
            "purchase_cost": self.purchase_cost,
            "purchase_date": self.purchase_date.isoformat(),
            "note": self.note,
            "warranty": self.warranty,
            "photo": self.photo,
            "actual_photo_name": self.actual_photo_name,
            "default_location": self.default_location
            
            }


class License():
    # id = Column(Integer, primary_key = True)
    # software_name = Column(Integer, nullable= False)
    # category_name = Column(String(100), nullable= True, default= " ")
    # product_key = Column(String, nullable= False)
    # seats = Column(String(50), nullable= False)
    # company = Column(String(100), nullable= True, default= " ")
    # manufacturer = Column(String(100), nullable= True, default=" ")
    # license_to_name = Column(String(100), nullable= False)
    # license_to_email = Column(String(255), nullable= False)
    # reassignable = Column(Boolean, nullable= False)
    # supplier = Column(String(100), nullable= True, default=" ")
    # order_number = Column(String(50), nullable= True, default = " ")
    # purchase_cost = Column(Float, nullable= False)
    # purchase_date = Column(Date, nullable= False)
    # expiration_date = Column(Date, nullable= False)
    # termination_date = Column(Date, nullable= True)
    # purchase_order_number = Column(String(50), nullable= True, default= "")
    # maintained = Column(Boolean, nullable= False)
    # note = Column(String, nullable= True, default= " ")
    # default_location = Column(String, nullable= False)
    


    # Constructor
    def __init__(
        self,
        software_name,
        category_name,
        product_key,
        seats,
        company,
        manufacturer,
        license_to_name,
        license_to_email,
        reassignable,
        supplier,
        order_number,
        purchase_cost,
        purchase_date,
        expiration_date,
        termination_date,
        purchase_order_number,
        maintained,
        default_location,
        note
        ):

        self.software_name = software_name
        self.category_name = category_name
        self.product_key = product_key
        self.seats = seats
        self.company = company
        self.manufacturer = manufacturer
        self.license_to_name = license_to_name
        self.license_to_email = license_to_email
        self.reassignable = reassignable
        self.supplier = supplier
        self.order_number = order_number
        self.purchase_cost = purchase_cost
        self.purchase_date = purchase_date
        self.expiration_date = expiration_date
        self.termination_date = termination_date
        self.purchase_order_number = purchase_order_number
        self.maintained = maintained
        self.note = note
        self.default_location = default_location


    def insert(self):
        # create new license
        db.session.add(self)
        db.session.commit()

    def update(self):
        # update existing license
        db.session.commit()


    def delete(self):
        # delete license
        db.session.delete(self)
        db.session.commit()


    
    def format(self):
        # json format of 
        # license data
        return {
            "license_id": self.id,
            "software_name": self.software_name,
            "category_name": self.category_name,
            "product_key": self.product_key,
            "seats": self.seats,
            "company": self.company,
            "manufacturer": self.manufacturer,
            "license_to_name": self.license_to_name,
            "license_to_email": self.license_to_email,
            "reassignable": self.reassignable,
            "supplier": self.supplier,
            "order_number": self.order_number,
            "purchase_cost": self.purchase_cost,
            "purchase_date": self.purchase_date.isoformat(),
            "expiration_date": self.expiration_date.isoformat(),
            "termination_date": self.termination_date.isoformat() if self.termination_date else "",
            "purchase_order_number": self.purchase_order_number,
            "maintained": self.maintained,
            "default_location": self.default_location,
            "note": self.note
        }






