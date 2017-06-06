import json

import xmltodict


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

    return payload


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

    return payload


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
