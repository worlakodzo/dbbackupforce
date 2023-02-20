import requests
import unittest
import os
unittest.defaultTestLoader.sortTestMethodsUsing = lambda *args: 1

# Define the base URL of the app
base_url = "http://worlako.jumpingcrab.com:8086"
# base_url = "http://192.168.1.123:5000"


# BEGIN test case order
# Order the execution of
# test case in order of
# declaration
def make_orderer():
    order = {}

    def ordered(f):
        order[f.__name__] = len(order)
        return f

    def compare(a, b):
        return [1, -1][order[a] < order[b]]

    return ordered, compare

ordered, compare = make_orderer()
unittest.defaultTestLoader.sortTestMethodsUsing = compare
# END test case order



class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.base_url = base_url

    @ordered
    def test_create_user(self):
        payload = {
                "username": "admintest",
                "password": "admintest",
                "phone": "0245000001",
                "email": "admin@uasset.com",
                "full_name": "Admin Test",
                "is_active": True,
                "is_admin": True
            }

        res = requests.post(f"{base_url}/users", json=payload)
        assert res.status_code == 201, f"Expected 201, got {res.status_code}"

        user = res.json()
        assert user["success"] == True, f"Expected 'True', got {user['success']}"

        os.environ['user_id'] =  user["_id"]

    @ordered
    def test_get_user(self):
        user_id = os.environ.get("user_id", "")
        res = requests.get(f"{base_url}/users/{user_id}")

        assert res.status_code == 200, f"Expected 200, got {res.status_code}"
        user = res.json()['data']
        assert user["full_name"] == "Admin Test", f"Expected 'Admin Test', got {user['full_name']}"


    @ordered
    def test_update_user(self):
        user_id = os.environ.get("user_id", "")

        payload = { 
            "action_type": "update-user-data",
            "full_name": "Updated Admin Test",
            "about": "Test",
            "job_title": "Test",
            "address": "Test Street",
            "phone": "0215455555",
            "email": "test@test.com",
            "twitter_link": "",
            "facebook_link": "",
            "linkedin_link": ""

            }
        
        res = requests.put(f"{base_url}/users/{user_id}", json=payload)

        assert res.status_code == 200, f"Expected 200, got {res.status_code}"

        user = res.json()['data']
        assert user["full_name"] == "Updated Admin Test", f"Expected 'Updated Admin Test', got {user['full_name']}"




    @ordered
    def test_delete_user(_id):
        res = requests.delete(f"{base_url}/users/{_id}")
        assert res.status_code == 204, f"Expected 204, got {res.status_code}"




class ManageCredentialTestCase(unittest.TestCase):

    def setUp(self):
        self.base_url = base_url


    @ordered
    def test_create_manage_credential(self):
        payload = {
            "_id": "database_engine_id59",
            "type": "database_engines",
            "engine_or_storage_provider": {
            "_id": "mysql",
            "name": "MySQL",
            "description": "",
            "type": "relational",
            "image": "db/mysql-logo.png"
        },
        "credential": {
            "database_name": "my_db",
            "database_host": "localhost",
            "database_user": "my_db",
            "database_password": "my_db",
            "database_port": "3036"
        }
        
        }

        res = requests.post(f"{base_url}/credentials", json=payload)
        assert res.status_code == 201, f"Expected 201, got {res.status_code}"

        json_data = res.json()
        credential = json_data['credential']
        assert json_data["success"] == True, f"Expected 'True', got {json_data['success']}"
        os.environ["credential_id"] = credential["_id"]


    @ordered
    def test_get_manage_credentials(self):
        res = requests.get(f"{base_url}/credentials")

        assert res.status_code == 200, f"Expected 200, got {res.status_code}"

        data = res.json()
        credentials = data["credentials"]
        credential_types = data["credential_types"]

        assert data["success"] == True, f"Expected 'True', got {data['success']}"
        assert len(credentials) > 0, f"Expected 'Credentials Count > 0 ', got {len(credentials)}"
        assert len(credential_types) > 0, f"Expected 'Credential Types > 0', got {len(credential_types)}"


    @ordered
    def test_get_manage_credential(self):

        credential_id = os.environ.get("credential_id", "")
        res = requests.get(f"{base_url}/credentials/{credential_id}")

        assert res.status_code == 200, f"Expected 200, got {res.status_code}"

        data = res.json()
        credential = data["credential_data"]

        assert data["success"] == True, f"Expected 'True', got {data['success']}"
        assert credential['type'] == "database_engines", f"Expected 'database_engines', got {credential['type']}"


    @ordered
    def test_update_manage_credential(self):

        credential_id = os.environ.get("credential_id", "")
        payload = {

            "credential": {
                "database_name": "my_db_change_name",
                "database_host": "localhost",
                "database_user": "my_db",
                "database_password": "my_db",
                "database_port": "3036"
            }
        }

        res = requests.put(f"{base_url}/credentials/{credential_id}", json=payload)
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"

        json_data = res.json()
        credential = json_data['credential_data']['credential']
        print (credential)
        
        assert json_data["success"] == True, f"Expected 'True', got {json_data['success']}"
        assert credential["database_name"] == "my_db_change_name", f"Expected 'my_db_change_name', got {credential['database_name']}"


    @ordered
    def test_u_delete_manage_credential(self):

        credential_id = os.environ.get("credential_id", "")

        res = requests.delete(f"{base_url}/credentials/{credential_id}")
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"

        json_data = res.json()

        
        assert json_data["success"] == True, f"Expected 'True', got {json_data['success']}"
        assert json_data["credential_id"] == credential_id, f"Expected '{credential_id}', got {json_data['credential_id']}"






# Run the tests
if __name__ == "__main__":
    unittest.main(verbosity=2)