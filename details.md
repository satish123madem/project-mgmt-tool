# Permissions / Constraints

**User** 
    
    1. can be created by anyone for self. 
    2. Can be modified by owner / superuser
    3. can be soft deletd by owner / super user
    4. can be authenticated by owner / super user
    5. undo delete can be done by super user only. 

**Role**
    
    1. Can be created/updated/deleted by user only
    2. higher roles can see lower role

**User logins**

    1. No end point explicitly available to create/update/delete
    2. can be retrived by owner
    3. All logins can be seen by super user




# API Endpoints

**/auth/login/**

    This endpoint wil be used to authenticate user

    allowed_methods : POST
    payload : 
        {
            "email" : "valid email id",
            "password" : "valid password"
        }

    expected outputs: 

    1. bad request      400      incorrect payload
    2. user not found   403      incorrect email id
    3. invalid password 403      incorrect password


**/auth/register/**

    this api helps to create user in database.

    allowed_methods : POST
    payload
    {
        "email": "valid email id",
        "password" : "password of 8 to 16 chars",
        "conf_password": "same a password",
        "first_name" : "string",
        "last_name" : "string",
        "role" : "int"
    } 

**/auth/user-detail/**

    this is a combined API to perform RUD (Retrive, updte and delete) user objects
    
    **Authentication credentials are required (JWT token) with Bearer prefix

    GET : 
    returns self user details
---
    PUT :
    payload
    {
        'password' : 'user password',
        'field_name_to_update' : 'field_value to update'
    }
---
    PATCH :
    this is to update the password alone.

    payload : 
    {
        'password' : 'user old password',
        'new_password' : 'new password to change',
        'conf_new_password' : 'confirm new password'
    }
---
    DELETE : 
    this endpoint will make the user status inactive further user will not be able to login or access any resource. 

    payload : 
    {
        'password' : 'user current password'
    }