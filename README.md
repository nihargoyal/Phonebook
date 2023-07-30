# DJANGO PhoneBook

Steps to run the API
## Install dependencies
```
pip3 install requirements.txt
```

## Runserver
```
python3 manage.py runserver
```
## Test the API
```
Route: http://localhost:8080/api/register/
Request Type: POST
Data:

    {
        "username": "john_doe",
        "password": "secretpassword",
        "phone_number": "1234567890",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com"
    }
```
## YOU HAVE TO LOGIN FOR PERMISSION TO ACCESS OTHER APIs
```
Route: http://localhost:8080/api/login/
Request Type: POST
Data:

    {
        "username":"john_doe",
        "password":"secretpassword"
    }
```

```

### To view all the contacts
```
Public Route: http://localhost:8080/api/contact/
Request Type: GET
```

To mark a contact as SPAM
```
Private Route: http://localhost:8080/api/spam/
Request Type: POST
Data:
    {
        "phone_number": "1234567890"
    }
```

To search by name or phone_number
```
Private Route: http://localhost:8080/api/search/?name=john
Request Type: GET
```
```
Private Route: http://localhost:8080/search/?phone_number=1234567890
Request Type: GET
```
