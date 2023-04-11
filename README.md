# Starter App Using Python in Flask framework
#### This app is used to store the address of users

## Server Setup
* Install Python 3.9 or 3.10
* Create and activate Virtual Environment
* Install requirements
```commandline
pip install -r requirements.txt
```
* Migrate Database
```commandline
python migrate.py
```
* Run Server
```commandline
python run_server.py
```

## RestAPIs
#### All APIs are in below postman collection. 
File name: **Starter App.postman_collection.json** 
Export this file in your postman or you can follow the below steps.

Go to http://127.0.0.1:5000, to check if server is running or not.
```json
{
    "message": "server is up"
}
```

1. First of all sign up using POST request http://127.0.0.1:5000/signup and in the request body you have to pass.
```text
curl --location 'http://127.0.0.1:5000/signup' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "dixit",
    "email": "dixit@gmail.com",
    "password": "12345678",
    "role": "user"
}'
```
Response
```json
{
    "status": "success",
    "user_id": 2
}
```

2. Now login using your email and password using POST API http://127.0.0.1:5000/login and pass details in request body.
```text
curl --location 'http://127.0.0.1:5000/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "dixit@gmail.com",
    "password": "12345678"
}'
```
Response
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3ODg4MjA1NiwianRpIjoiNzQwMWZlNjYtNjc3Yy00MGFkLWI2NzItZDA0YzU2ZjViOTFhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VyX2lkIjoyfSwibmJmIjoxNjc4ODgyMDU2LCJleHAiOjE2Nzg4ODIzNTZ9.IgUKVeJnFXhZHbkAFepEa2DKNNFVWu70TKAiSQ9WjHY",
    "expire_in": 300,
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3ODg4MjA1NiwianRpIjoiN2VmZjQxYjUtZWY5Ni00MjFhLWFhMWYtMjRjZTNhNGUzMzNkIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsidXNlcl9pZCI6Mn0sIm5iZiI6MTY3ODg4MjA1NiwiZXhwIjoxNjc4OTY4NDU2fQ.gjQaJRgdebuIIiMY2kOMQXmNyUVh310P3MsAxcXYlDo"
}
```
3. Change Password using PUT API http://127.0.0.1:5000/change_password
```text
curl --location --request PUT 'http://127.0.0.1:5000/change_password' \
--header 'x-access-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOjEsImV4cCI6MTY3ODg3MTQ0Mn0.nwKrRHBGQIYNT3WtbwFKpPg408AwYXhzcJFQhqipBtc' \
--header 'Content-Type: application/json' \
--data '{
    "old_password": "12345678",
    "new_password": "987654321"
}'
```
Response
```json
{
    "status": "success"
}
```

4. Get access token using refresh token if access token is expired using GET API http://127.0.0.1:5000/refresh
```text
curl --location 'http://127.0.0.1:5000/refresh' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3ODg4MjA1NiwianRpIjoiN2VmZjQxYjUtZWY5Ni00MjFhLWFhMWYtMjRjZTNhNGUzMzNkIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOnsidXNlcl9pZCI6Mn0sIm5iZiI6MTY3ODg4MjA1NiwiZXhwIjoxNjc4OTY4NDU2fQ.gjQaJRgdebuIIiMY2kOMQXmNyUVh310P3MsAxcXYlDo'
```
Response
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3ODg4MjkxNCwianRpIjoiMjk5NTQxODUtYmVhZi00NWVmLTk0NDgtMzViOWIyZTI0ODcxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VyX2lkIjoyfSwibmJmIjoxNjc4ODgyOTE0LCJleHAiOjE2Nzg4ODMyMTR9.5KQrzuEDZXrzpi8GNcAP_CyTMuxI-EXT-uEfe5muTmY",
    "expire_in": 300
}
```
5. Now you can add your address using POST API http://127.0.0.1:5000/address
```text
curl --location 'http://127.0.0.1:5000/address' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3ODg4MjA1NiwianRpIjoiNzQwMWZlNjYtNjc3Yy00MGFkLWI2NzItZDA0YzU2ZjViOTFhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VyX2lkIjoyfSwibmJmIjoxNjc4ODgyMDU2LCJleHAiOjE2Nzg4ODIzNTZ9.IgUKVeJnFXhZHbkAFepEa2DKNNFVWu70TKAiSQ9WjHY' \
--header 'Content-Type: application/json' \
--data '{
    "country": "India",
    "house_no_and_street": "74, ward 4",
    "landmark": "Near govt school",
    "pin_code": 121106,
    "type": "home"

}'
```
Response 
```json
{
    "address_id": 1,
    "status": "success"
}
```
6. Update address using PUT API. http://127.0.0.1:5000/address
```text
curl --location --request PUT 'http://127.0.0.1:5000/address' \
--header 'x-access-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOjEsImV4cCI6MTY3ODg3MzMxMH0.oAK4631KqpUOseupqQb_yELOT_pbghK0mAH_oWgv-Zs' \
--header 'Content-Type: application/json' \
--data '{
    "address_id": 1,
    "pin_code": 111111,
    "type": "work"
}'
```
Response
```json
{
    "message": "success"
}
```
7. Get list of address using GET API http://127.0.0.1:5000/addresses
Using ADMIN role access token then you can get the addresses 
of all users as well as for a particular user by passing the user_id
http://127.0.0.1:5000/addresses/<user_id>
```text
curl --location 'http://127.0.0.1:5000/addresses' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3ODg4MjA1NiwianRpIjoiNzQwMWZlNjYtNjc3Yy00MGFkLWI2NzItZDA0YzU2ZjViOTFhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VyX2lkIjoyfSwibmJmIjoxNjc4ODgyMDU2LCJleHAiOjE2Nzg4ODIzNTZ9.IgUKVeJnFXhZHbkAFepEa2DKNNFVWu70TKAiSQ9WjHY'
```
Response (list of addresses)
```json
[
    {
        "address_id": 1,
        "country": "India",
        "house_no_and_street": "74, ward 4",
        "landmark": "Near govt school",
        "pin_code": "111111",
        "created_at": "Wed, 15 Mar 2023 12:07:45 GMT",
        "submitter_name": "dixit",
        "type": "work",
        "user_id": 2,
        "updated_at": "Wed, 15 Mar 2023 14:57:37 GMT"
    }
]
```
8. Delete Address using DELETE API http://127.0.0.1:5000/address/<address_id>
```text
curl --location --request DELETE 'http://127.0.0.1:5000/address/1' \
--header 'x-access-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOjEsImV4cCI6MTY3ODg3NTU4M30.bpfLOGeeOv7x1GJ4SaoNfrzWD1VoiCM4vLoWsuGneps'
```
Response
```json
{
    "message": "success"
}
```

9. Logout using delete API http://127.0.0.1:5000/logout
```text
curl --location --request DELETE 'http://127.0.0.1:5000/logout' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4MDE4MTY3NywianRpIjoiZGVjYzQ2NWQtNzUzNC00YTFiLWE4Y2UtMThjZjg5YTUyNDI2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VyX2lkIjoxfSwibmJmIjoxNjgwMTgxNjc3LCJleHAiOjE2ODAyMDMyNzd9.wWfl9HFmoJzyuH5vk7wTi1SblsDrbZTzqfpGs6QaEjE'
```
Response
```json
{
    "msg": "Access token successfully revoked"
}
```

## Unit testing
1. Auth routers unit testing 
```commandline
(venv) C:\Users\puneet dixit\Desktop\starter app>python -m unittest unit_testing.auth_router_tests.AuthRouterTest
........
----------------------------------------------------------------------
Ran 8 tests in 1.349s

OK
```
2. Main routers unit testing

```commandline
(venv) C:\Users\puneet dixit\Desktop\starter app>python -m unittest unit_testing.main_router_tests.MainRouterTest
......
----------------------------------------------------------------------
Ran 6 tests in 1.173s

OK
```
3. Database Models unit testing
```commandline

(venv) C:\Users\puneet dixit\Desktop\starter app>python -m unittest unit_testing.models_tests.ModelsTests
..
----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
```