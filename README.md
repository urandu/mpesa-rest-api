# Mpesa Rest API (MRA)
mpesa rest api converts the mpesa api to a RESTful API that is easy for developers to use instead of the current SOAP web service provided by mpesa.


## Installation

### Requirements

`` -Python 2.7 ``

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

### Docker (has a bug)

To run the application via using docker (docker should be installed on your machine) : 
```
git clone https://github.com/urandu/mpesa-rest-api.git
cd mpesa-rest-api

docker-compose up

```

## C2B Validation And Confirmation

For validation and confirmation you need to have validation end point that will receive validation requests in json form. 
You also need to have a confirmation endpoint in your application that will receive confirmation requests from MRA(mpesa rest api).

When requesting for validation and confirmation G2 API access from safaricom, they will ask you for two endpoints, the validation and the confirmation endpoints.

Below are the endpoints you should give them once you you deploy MRA 

**Confirmation endpoint** = **`http://your_application_ip_address/confirmation/`**

**Validation endpoint** = **`http://your_application_ip_address/validation/`**

### validation workflow and payloads

-when a users makes a paybill payment via mpesa from his/her phone, mpesa will send a validation request to MRA. 

-MRA will parse the SOAP request and convert it to json.

-MRA will then post the json to the validation endpoint provided in the settings.py file. below is a sample (format) of the json payload:
```
{
  "trans_time": "20140227082020",
  "kycinfo": "[{\"KYCName\": \"[Personal Details][First Name]\", \"KYCValue\": \"Hoiyor\"}, {\"KYCName\": \"[Personal Details][Middle Name]\", \"KYCValue\": \"G\"}, {\"KYCName\": \"[Personal Details][Last Name]\", \"KYCValue\": \"Chen\"}]",
  "trans_amount": "123.00",
  "trans_type": "PayBill",
  "msisdn": "254722703614",
  "invoive_number": null,
  "paybill_number": "12345",
  "trans_id": "1234560000007031",
  "account_number": "hjhdjhd"
}

```
-The response that MRA expects from the validation endpoint is :

The result_code returned by the validation endpoint should be 0 for success otherwise, use one of the codes below to describe the error:
 ```
result_code       result_description
C2B00011          Invalid MSISDN
C2B00012          Invalid Account number
C2B00013          Invalid Amount
C2B00014          Invalid KYC details
C2B00015          Invalid Shortcode
C2B00016          Other Error

```

Example response:
```
{
     "result_code": "0"
     "result_description": "sucessful validation" 
     "custom_trans_id": "id from your application" 
}

```


## Online checkout (C2B)

(coming soon)

## B2C

(coming soon)

## B2B 

(coming soon)
