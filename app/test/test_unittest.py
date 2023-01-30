import requests
import json

# Define the base URL of the app
base_url = "http://54.187.146.17:8086"


# Test creating a user
def test_create_user():
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
    assert user["success"] == True, f"Expected 'True', got '{user['success']}'"
    return user["_id"]


# Test retrieving a user
def test_get_user(_id):
    res = requests.get(f"{base_url}/users/{_id}")

    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    user = res.json()
    assert user["full_name"] == "Admin Test", f"Expected 'Admin Test', got '{user['full_name']}'"


# Test updating a user
def test_update_user(_id):
    payload = { 
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
    
    res = requests.put(f"{base_url}/users/{_id}", json=payload)

    assert res.status_code == 200, f"Expected 200, got {res.status_code}"

    user = res.json()
    assert user["full_name"] == "Updated Admin Test", f"Expected 'Updated Admin Test', got '{user['full_name']}'"


# Test deleting a user
def test_delete_user(_id):
    res = requests.delete(f"{base_url}/users/{_id}")
    assert res.status_code == 204, f"Expected 204, got {res.status_code}"


# Run the tests
if __name__ == "__main__":
    user_id = test_create_user()
    test_get_user(user_id)
    test_update_user(user_id)
    test_delete_user(user_id)

    print("4/4 tests passed")