# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from urllib2 import Request, urlopen

import requests
from django.http import HttpResponse
from django.utils.http import urlencode
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from zeep import Client
import xmltodict
import json
from django.shortcuts import render

# Create your views here.
from mpesa import settings


@csrf_exempt
def index(request):
    client = Client('http://www.webservicex.net/ConvertSpeed.asmx?WSDL')
    result = client.service.ConvertSpeed(
        100, 'kilometersPerhour', 'milesPerhour')
    payload = \
        {
            "result_code": "badam",
            "result_description": "ssss",
            "custom_trans_id": "ssss"
        }
    return HttpResponse(json.dumps(payload))


@csrf_exempt
def validation(request):


    o = xmltodict.parse(request.body.decode('utf-8'))
    o = json.loads(json.dumps(o))
    trans_type = \
    o['soapenv:Envelope']['soapenv:Body']['ns1:C2BPaymentValidationRequest'][
        'TransactionType']
    trans_id = \
    o['soapenv:Envelope']['soapenv:Body']['ns1:C2BPaymentValidationRequest'][
        'TransID']
    trans_time = \
    o['soapenv:Envelope']['soapenv:Body']['ns1:C2BPaymentValidationRequest'][
        'TransTime']
    trans_amount = \
    o['soapenv:Envelope']['soapenv:Body']['ns1:C2BPaymentValidationRequest'][
        'TransAmount']
    business_short_code = \
    o['soapenv:Envelope']['soapenv:Body']['ns1:C2BPaymentValidationRequest'][
        'BusinessShortCode']
    bill_ref_number = \
    o['soapenv:Envelope']['soapenv:Body']['ns1:C2BPaymentValidationRequest'][
        'BillRefNumber']
    invoice_number = \
    o['soapenv:Envelope']['soapenv:Body']['ns1:C2BPaymentValidationRequest'][
        'InvoiceNumber']
    msisdn = \
    o['soapenv:Envelope']['soapenv:Body']['ns1:C2BPaymentValidationRequest'][
        'MSISDN']
    kyc_info = \
    o['soapenv:Envelope']['soapenv:Body']['ns1:C2BPaymentValidationRequest'][
        'KYCInfo']

    url = settings.VALIDATION_URL  # Set destination URL here  nbnbn

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
    response = requests.post(url, data=payload)
    response.content
    if response.ok:
        """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:c2b="http://cps.huawei.com/cpsinterface/c2bpayment">
   <soapenv:Header/>
   <soapenv:Body>
      <c2b:C2BPaymentValidationResult>
        <ResultCode>0</ResultCode>
	   <ResultDesc>Service processing successful</ResultDesc>
	   <ThirdPartyTransID>1234560000088888</ThirdPartyTransID>
      </c2b:C2BPaymentValidationResult>
   </soapenv:Body>
</soapenv:Envelope>
"""
        response_json = json.loads(response.content)
        result_code = response_json['result_code']
        result_description = response_json['result_description']
        custom_transaction_id = response_json['custom_trans_id']

        pass
    xml_response = '<soapenv:Envelope xmlns:soapenv="http:' \
                   '//schemas.xmlsoap.org/soap/envelope/" ' \
                   'xmlns:c2b="' \
                   'http://cps.huawei.com/cpsinterface/c2bpayment">' \
                   '<soapenv:Header/>' \
                   '<soapenv:Body><c2b:C2BPaymentValidationResult>' \
                   '<ResultCode>'+str(result_code)+'</ResultCode><ResultDesc>' \
                   + str(result_description) + '</ResultDesc>' \
                   '<ThirdPartyTransID>' + str(custom_transaction_id) + \
                   '</ThirdPartyTransID>' \
                   '</c2b:C2BPaymentValidationResult>' \
                   '</soapenv:Body></soapenv:Envelope>'
    print(response.text)  # TEXT/HTML
    print(response.status_code, response.reason)  # HTTP
    # return HttpResponse(str(json.dumps(kyc_info)))
    return HttpResponse(xml_response, content_type='application/xml')


class MpesaValidation(APIView):
    def post(self, request, format=None):
        o = xmltodict.parse(request.body.decode('utf-8'))
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

        url = settings.VALIDATION_URL  # Set destination URL here  nbnbn

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
        response = requests.post(url, data=payload)
        response.content
        if response.ok:
            """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:c2b="http://cps.huawei.com/cpsinterface/c2bpayment">
       <soapenv:Header/>
       <soapenv:Body>
          <c2b:C2BPaymentValidationResult>
            <ResultCode>0</ResultCode>
           <ResultDesc>Service processing successful</ResultDesc>
           <ThirdPartyTransID>1234560000088888</ThirdPartyTransID>
          </c2b:C2BPaymentValidationResult>
       </soapenv:Body>
    </soapenv:Envelope>
    """
            response_json = json.loads(response.content)
            result_code = response_json['result_code']
            result_description = response_json['result_description']
            custom_transaction_id = response_json['custom_trans_id']

            pass
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
        print(response.text)  # TEXT/HTML
        print(response.status_code, response.reason)  # HTTP
        # return HttpResponse(str(json.dumps(kyc_info)))
        return Response(xml_response, content_type='application/xml')
