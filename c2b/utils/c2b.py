import base64
import hashlib
import json
import uuid

import time
import xmltodict

from mpesa import settings


def parse_validation_request(xml_string):
    o = xmltodict.parse(xml_string)
    o = json.loads(json.dumps(o))
    trans_type = \
        o['soapenv:Envelope']['soapenv:Body'][
            'ns1:C2BPaymentValidationRequest'][
            'TransactionType']
    trans_id = \
        o['soapenv:Envelope']['soapenv:Body'][
            'ns1:C2BPaymentValidationRequest'][
            'TransID']
    trans_time = \
        o['soapenv:Envelope']['soapenv:Body'][
            'ns1:C2BPaymentValidationRequest'][
            'TransTime']
    trans_amount = \
        o['soapenv:Envelope']['soapenv:Body'][
            'ns1:C2BPaymentValidationRequest'][
            'TransAmount']
    business_short_code = \
        o['soapenv:Envelope']['soapenv:Body'][
            'ns1:C2BPaymentValidationRequest'][
            'BusinessShortCode']
    bill_ref_number = \
        o['soapenv:Envelope']['soapenv:Body'][
            'ns1:C2BPaymentValidationRequest'][
            'BillRefNumber']
    invoice_number = \
        o['soapenv:Envelope']['soapenv:Body'][
            'ns1:C2BPaymentValidationRequest'][
            'InvoiceNumber']
    msisdn = \
        o['soapenv:Envelope']['soapenv:Body'][
            'ns1:C2BPaymentValidationRequest'][
            'MSISDN']
    kyc_info = \
        o['soapenv:Envelope']['soapenv:Body'][
            'ns1:C2BPaymentValidationRequest'][
            'KYCInfo']

    payload = {
        'trans_type': trans_type,
        'trans_time': trans_time,
        'trans_id': trans_id,
        'trans_amount': trans_amount,
        'paybill_number': business_short_code,
        'account_number': bill_ref_number,
        'msisdn': msisdn,
        'kycinfo': json.dumps(kyc_info),
        'invoive_number': invoice_number
    }

    return json.dumps(payload)


def parse_validation_response(json_string):
    response_json = json.loads(json_string)
    result_code = response_json['result_code']
    result_description = response_json['result_description']
    custom_transaction_id = response_json['custom_trans_id']

    xml_response = '<soapenv:Envelope xmlns:soapenv="http:' \
                   '//schemas.xmlsoap.org/soap/envelope/" ' \
                   'xmlns:c2b="' \
                   'http://cps.huawei.com/cpsinterface/c2bpayment">' \
                   '<soapenv:Header/>' \
                   '<soapenv:Body><c2b:C2BPaymentValidationResult>' \
                   '<ResultCode>' + str(
        result_code) + '</ResultCode><ResultDesc>' \
                   + str(result_description) + '</ResultDesc>' \
                                               '<ThirdPartyTransID>' + str(
        custom_transaction_id) + \
                   '</ThirdPartyTransID>' \
                   '</c2b:C2BPaymentValidationResult>' \
                   '</soapenv:Body></soapenv:Envelope>'
    return xml_response


def parse_confirmation_request(xml_string):
    o = xmltodict.parse(xml_string)
    o = json.loads(json.dumps(o))
    trans_type = \
        o['soapenv:Envelope']['soapenv:Body'][
            'ns1:C2BPaymentConfirmationRequest'][
            'TransType']
    trans_id = \
        o['soapenv:Envelope']['soapenv:Body'][
            'ns1:C2BPaymentConfirmationRequest'][
            'TransID']
    trans_time = \
        o['soapenv:Envelope']['soapenv:Body'][
            'ns1:C2BPaymentConfirmationRequest'][
            'TransTime']
    trans_amount = \
        o['soapenv:Envelope']['soapenv:Body'][
            'ns1:C2BPaymentConfirmationRequest'][
            'TransAmount']
    business_short_code = \
        o['soapenv:Envelope']['soapenv:Body'][
            'ns1:C2BPaymentConfirmationRequest'][
            'BusinessShortCode']
    bill_ref_number = \
        o['soapenv:Envelope']['soapenv:Body'][
            'ns1:C2BPaymentConfirmationRequest'][
            'BillRefNumber']
    msisdn = \
        o['soapenv:Envelope']['soapenv:Body'][
            'ns1:C2BPaymentConfirmationRequest'][
            'MSISDN']
    kyc_info = \
        o['soapenv:Envelope']['soapenv:Body'][
            'ns1:C2BPaymentConfirmationRequest'][
            'KYCInfo']

    payload = {
        'trans_type': trans_type,
        'trans_time': trans_time,
        'trans_id': trans_id,
        'trans_amount': trans_amount,
        'paybill_number': business_short_code,
        'account_number': bill_ref_number,
        'msisdn': msisdn,
        'kycinfo': json.dumps(kyc_info)
    }

    return json.dumps(payload)


def parse_confirmation_response():
    xml_response = '<soapenv:Envelope xmlns:soapenv="http:' \
                   '//schemas.xmlsoap.org/soap/envelope/" ' \
                   'xmlns:c2b="' \
                   'http://cps.huawei.com/cpsinterface/c2bpayment">' \
                   '<soapenv:Header/>' \
                   '<soapenv:Body> ' \
                   '<c2b:C2BPaymentConfirmationResult>' \
                   'C2B Payment Transaction successfully received.' \
                   '</c2b:C2BPaymentConfirmationResult>' \
                   '</soapenv:Body></soapenv:Envelope>'
    return xml_response


def parse_checkout_request_body(request):
    merchant_transaction_id = request.POST.get('merchant_transaction_id')
    if not merchant_transaction_id:
        merchant_transaction_id = uuid.uuid4()
    reference_id = request.POST.get('account_number')
    amount = request.POST.get('amount')
    msisdn = request.POST.get('msisdn')
    timestamp = str(int(time.time()))
    xml_string = '<soapenv:Envelope' \
                 ' xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"' \
                 ' xmlns:tns="tns:ns">' \
                 '<soapenv:Header>' \
                 '<tns:CheckOutHeader>' \
                 '<MERCHANT_ID>' + settings.MERCHANT_ID + '</MERCHANT_ID>' \
                                                          '<PASSWORD>' \
                 + str(base64.b64encode(hashlib.
                                        sha256(settings.MERCHANT_ID +
                                               settings.MERCHANT_PASSKEY
                                               + timestamp).
                                        hexdigest())).upper() + \
                 '</PASSWORD>' \
                 '<TIMESTAMP>' \
                 + timestamp + \
                 '</TIMESTAMP>' \
                 '</tns:CheckOutHeader>' \
                 '</soapenv:Header>' \
                 '<soapenv:Body>' \
                 '<tns:processCheckOutRequest>' \
                 '<MERCHANT_TRANSACTION_ID>' \
                 + merchant_transaction_id + \
                 '</MERCHANT_TRANSACTION_ID>' \
                 '<REFERENCE_ID>' \
                 + reference_id + \
                 '</REFERENCE_ID>' \
                 '<AMOUNT>' + amount + '</AMOUNT>' \
                                       '<MSISDN>' + msisdn + '</MSISDN>' \
                                                             '<!--Optional:-->' \
                                                             '<ENC_PARAMS></ENC_PARAMS>' \
                                                             '<CALL_BACK_URL>' \
                 + settings.ONLINE_CHECKOUT_CALLBACK_URL + \
                 '/test</CALL_BACK_URL>' \
                 '<CALL_BACK_METHOD>xml</CALL_BACK_METHOD>' \
                 '<TIMESTAMP>' + timestamp + '</TIMESTAMP>' \
                                             '</tns:processCheckOutRequest>' \
                                             '</soapenv:Body>' \
                                             '</soapenv:Envelope>'

    return xml_string


def parse_checkout_response(xml_response):

    response = xmltodict.parse(xml_response)
    response = json.loads(json.dumps(response))
    output = {
        "trx_id": response['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ns1:processCheckOutResponse']['TRX_ID'],
        "return_code": response['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ns1:processCheckOutResponse']['RETURN_CODE'],
        "description": response['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ns1:processCheckOutResponse']['DESCRIPTION']
    }
    return output


def package_confirmation_request(response_dict):

    timestamp = str(int(time.time()))
    xml_string = '<soapenv:Envelope ' \
                 'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" ' \
                 'xmlns:tns="tns:ns">' \
                 '<soapenv:Header><tns:CheckOutHeader>' \
                 '<MERCHANT_ID>' + settings.MERCHANT_ID + '</MERCHANT_ID>' \
                 '<PASSWORD>' \
                 + str(base64.b64encode(hashlib.
                                        sha256(settings.MERCHANT_ID +
                                               settings.MERCHANT_PASSKEY
                                               + timestamp).
                                        hexdigest())).upper() + \
                 '</PASSWORD>' \
                 '<TIMESTAMP>' + timestamp + '</TIMESTAMP>' \
                 '</tns:CheckOutHeader>' \
                 '</soapenv:Header>' \
                 '<soapenv:Body>' \
                 '<tns:transactionConfirmRequest>' \
                 '<!--Optional:-->' \
                 '<TRX_ID>'+str(response_dict.get('trx_id'))+'</TRX_ID>' \
                 '<!--Optional:-->' \
                 '<MERCHANT_TRANSACTION_ID>' \
                 '' \
                 '</MERCHANT_TRANSACTION_ID>' \
                 '</tns:transactionConfirmRequest>' \
                 '</soapenv:Body></soapenv:Envelope>'
    return xml_string


def unpackage_confirmation_request(response_dict):

    timestamp = str(int(time.time()))
    xml_string = '<soapenv:Envelope ' \
                 'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" ' \
                 'xmlns:tns="tns:ns">' \
                 '<soapenv:Header><tns:CheckOutHeader>' \
                 '<MERCHANT_ID>' + settings.MERCHANT_ID + '</MERCHANT_ID>' \
                 '<PASSWORD>' \
                 + str(base64.b64encode(hashlib.
                                        sha256(settings.MERCHANT_ID +
                                               settings.MERCHANT_PASSKEY
                                               + timestamp).
                                        hexdigest())).upper() + \
                 '</PASSWORD>' \
                 '<TIMESTAMP>' + timestamp + '</TIMESTAMP>' \
                 '</tns:CheckOutHeader>' \
                 '</soapenv:Header>' \
                 '<soapenv:Body>' \
                 '<tns:transactionConfirmRequest>' \
                 '<!--Optional:-->' \
                 '<TRX_ID>'+str(response_dict.get('trx_id'))+'</TRX_ID>' \
                 '<!--Optional:-->' \
                 '<MERCHANT_TRANSACTION_ID>' \
                 '' \
                 '</MERCHANT_TRANSACTION_ID>' \
                 '</tns:transactionConfirmRequest>' \
                 '</soapenv:Body></soapenv:Envelope>'
    return xml_string
