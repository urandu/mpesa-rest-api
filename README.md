# Mpesa Rest API (MRA)
mpesa rest api converts the mpesa api to a RESTful API that is easy for developers to use instead of the current SOAP web service provided by mpesa.


## Installation

### Requirements

`` -Python 2.7 or 3.x ``



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
(examples are coming shortly...)