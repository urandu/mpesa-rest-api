# Mpesa Rest API (MRA)
mpesa rest api converts the mpesa api to a RESTful API that is easy for developers to use instead of the current SOAP web service provided by mpesa.


## Installation

### Requirements

`` -Python 2.7 or 3.x ``

### Configuration

In the settings file `` mpesa/settings.py`` scroll to the bottom and replace the following urls _VALIDATION_URL = "http://127.0.0.1:8000/c2b/"_ and _CONFIRMATION_URL = "http://127.0.0.1:8000/c2b/"_
 with the validation and confirmation endpoint to your application respectively  

example:

replace 
```
VALIDATION_URL = "http://127.0.0.1:8000/c2b/"
CONFIRMATION_URL = "http://127.0.0.1:8000/c2b/"

```
with
```
VALIDATION_URL = "http://myapplication/validate_mpesa_payment/"
CONFIRMATION_URL = "http://myapplication/confirm_mpesa_payment/"

```

### Development

```` 
git clone https://github.com/urandu/mpesa-rest-api.git
cd mpesa-rest-api
pip install -r requirements.txt
python manage.py runserver
````

### Production (not ready for production)
```` 
git clone https://github.com/urandu/mpesa-rest-api.git
cd mpesa-rest-api
pip install -r requirements.txt
./start.sh
````


## C2B Validation And Confirmation

For validation and confirmation you need to have validation end point that will receive validation requests in json form. 
You also need to have a confirmation endpoint in your application that will receive confirmation requests from MRA(mpesa rest api).

When requesting for validation and confirmation G2 API access from safaricom, they will ask you for two endpoints, the validation and the confirmation endpoints.

Below are the endpoints you should give them once you you deploy MRA 

**Confirmation endpoint** = **`http://your_application_ip_address/confirmation/`**

**Validation endpoint** = **`http://your_application_ip_address/validation/`**



## Online checkout (C2B)

(coming soon)

## B2C

(coming soon)

## B2B 

(coming soon)
