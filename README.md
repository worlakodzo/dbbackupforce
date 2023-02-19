# backUpforce Plus

## Introduction:

The following API documentation provides information on how to access and utilize the backUpforce Plus. This documentation includes details on the various endpoints, request methods, and expected responses. With this information, developers and users can effectively interact with the system to create, read, update, and delete user information.


### GET /health
Return the status of the application server.

### Response:

- 200 OK:



## User API


### GET /users
Retrieve a list of all users.

### Response:

- 200 OK: List of users is returned.
```
{
    "success": True,
    "data": [

            {
                "_id":"6eb36cf0-194c-477c-b9aa-7d92faffbe47",
                "username":"example",
                "is_active":true,
                "is_admin":true,
                "full_name":"Example",
                "about":"",
                "job_title":"",
                "address":"",
                "phone":"0245000001",
                "email":"example@uasset.com",
                "photo":{
                    "storage_type":"local",
                    "path":"default.png"
                },
                "email_notification":{
                    "changes_made_to_account":false,
                    "new_assert_added":false,
                    "assert_expiring":false,
                    "security_notify":false
                },
                "social_link":{
                    "twitter":"",
                    "facebook":"",
                    "linkedin":""
                }
            }
    ]
}
```
- 404 NOT FOUND: No users found.


### GET /users/{user_id}
Retrieve information about a specific user by their ID.

### Path parameters:

- user_id: (required) The ID of the user.


### Response:

- 200 OK: User information is returned.
```
{
   "success":true,
   "data":{
      "_id":"6eb36cf0-194c-477c-b9aa-7d92faffbe47",
      "username":"example",
      "is_active":true,
      "is_admin":true,
      "full_name":"Example",
      "about":"",
      "job_title":"",
      "address":"",
      "phone":"0245000001",
      "email":"example@uasset.com",
      "photo":{
         "storage_type":"local",
         "path":"default.png"
      },
      "email_notification":{
         "changes_made_to_account":false,
         "new_assert_added":false,
         "assert_expiring":false,
         "security_notify":false
      },
      "social_link":{
         "twitter":"",
         "facebook":"",
         "linkedin":""
      },
      "photo_link":"/static/vol/media/img/default.png"
   }
}
```
- 404 NOT FOUND: User with the specified ID was not found.


### POST /users
Create a new user.

### Request body:

- name: (required) The name of the user.
- email: (required) The email of the user.
- password: (required) The password for the user.

### Response:

- 201 CREATED: The user was successfully created.
- 400 BAD REQUEST: Invalid request data.
- 409 CONFLICT: The email already exists in the system.


### PUT /users/{user_id}
Update an existing user by their ID.

### Path parameters:

- user_id: (required) The ID of the user.

### Request body:

- name: (optional) The name of the user.
- email: (optional) The email of the user.
- password: (optional) The password for the user.

### Response:

- 200 OK: The user was successfully updated.
- 400 BAD REQUEST: Invalid request data.
- 404 NOT FOUND: User with the specified ID was not found.


### DELETE /users/{user_id}
Delete an existing user by their ID.

Path parameters:

- user_id: (required) The ID of the user.

### Response:
- 200 OK: The user was successfully deleted.
- 404 NOT FOUND: User with the specified ID was not found.






### Reference 
- https://yashmehrotra.com/posts/building-minimal-docker-images-using-multi-stage-builds/
- https://gabnotes.org/lighten-your-python-image-docker-multi-stage-builds/