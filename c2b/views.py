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
from c2b.utils.c2b import parse_validation_request, parse_validation_response, \
    parse_confirmation_request, parse_confirmation_response, \
    parse_checkout_request_body, parse_checkout_response, \
    package_confirmation_request, unpackage_confirmation_request
from mpesa import settings

# This endpoint is a mock endpoint for confirmation and validation from MRA


@csrf_exempt
def index(request):

    payload = \
        {
            "result_code": "0",
            "result_description": "default description",
            "custom_trans_id": "3434344"
        }
    return HttpResponse(json.dumps(payload))


@csrf_exempt
def payment_request_mock_url(request):

    payload = '<SOAP-ENV:Envelope' \
              ' xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" ' \
              'xmlns:ns1="tns:ns"><SOAP-ENV:Body>' \
              '<ns1:processCheckOutResponse>'\
              '<RETURN_CODE>00</RETURN_CODE>' \
              '<DESCRIPTION>Success</DESCRIPTION>' \
              '<TRX_ID>cce3d32e0159c1e62a9ec45b67676200</TRX_ID>' \
              '<ENC_PARAMS/>' \
              '<CUST_MSG>' \
              'To complete this transaction, enter your Bonga ' \
              'PIN on your handset. if you don\'t have one dial *126*5# ' \
              'for instructions' \
              '</CUST_MSG>' \
              '</ns1:processCheckOutResponse>' \
              '</SOAP-ENV:Body>' \
              '</SOAP-ENV:Envelope>'
    return HttpResponse(payload)


@csrf_exempt
def payment_response_mock_url(request):

    payload = '<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="tns:ns">   <SOAP-ENV:Body>      <ns1:transactionConfirmResponse>         <RETURN_CODE>00</RETURN_CODE>         <DESCRIPTION>Success</DESCRIPTION>         <MERCHANT_TRANSACTION_ID/>         <TRX_ID>5f6af12be0800c4ffabb4cf2608f0808</TRX_ID>      </ns1:transactionConfirmResponse>   </SOAP-ENV:Body></SOAP-ENV:Envelope>'
    return HttpResponse(payload)


@csrf_exempt
def validation(request):

    if request.method == 'POST':

        payload = parse_validation_request(request.body.decode('utf-8'))

        url = settings.VALIDATION_URL

        response = requests.post(url, data=payload)

        if response.ok:

            xml_response = parse_validation_response(response.content)

            return HttpResponse(xml_response, content_type='application/xml')


@csrf_exempt
def confirmation(request):

    if request.method == 'POST':

        payload = parse_confirmation_request(request.body.decode('utf-8'))

        url = settings.CONFIRMATION_URL

        response = requests.post(url, data=payload)

        if response.ok:

            xml_response = parse_confirmation_response()

            return HttpResponse(xml_response, content_type='application/xml')


@csrf_exempt
def process_checkout(request):

    if request.method == 'POST':

        payload = parse_checkout_request_body(request)

        url = settings.MPESA_PROCESS_CHECKOUT_URL
        # todo investigate if content type is invalid
        response = requests.post(url, data=payload)
        if response.ok:
            response = parse_checkout_response(response.content)

            if response.get('return_code') == "00":
                confirmation_payload = package_confirmation_request(response)

                confirmation_response = requests.\
                    post(url, data=confirmation_payload)
                if confirmation_response.ok:
                    confirmation_response = unpackage_confirmation_request(confirmation_response.content)

                return HttpResponse(json.dumps(confirmation_response), content_type='application/json')
        # confirmation

        #
        # if response.ok:
        #
        #     xml_response = parse_confirmation_response()
        #
        #     return HttpResponse(xml_response, content_type='application/xml')


def online_checkout_callback(request):
    """
    MSISDN:254700000000
      AMOUNT:100
      M-PESA_TRX_DATE:2014-08-01 15:30:00
      M-PESA_TRX_ID:FG232FT0
      TRX_STATUS:Success
      RETURN_CODE:00
      DESCRIPTION:Transaction successful 
      MERCHANT_TRANSACTION_ID:134562       
      ENC_PARAMS:XXXXXXXXXXX    

    :param request: 
    :return: 
    """
    payload = {
        "msisdn": request.POST.get('MSISDN'),
        "amount": request.POST.get('M-PESA_TRX_DATE'),
        "date": request.POST.get('M-PESA_TRX_ID'),
        "mpesa_transaction_id": request.POST.get('TRX_STATUS'),
        "transaction_status": request.POST.get('RETURN_CODE'),
        "return_code": request.POST.get('DESCRIPTION'),
        "description": request.POST.get('MERCHANT_TRANSACTION_ID'),
        "merchant_transaction_id": request.POST.get('ENC_PARAMS')
    }

    url = settings.MERCHANT_ONLINE_CHECKOUT_CALLBACK

    response = requests.post(url, data=payload)

    if response.ok:

        return HttpResponse(response.status_code, content_type='application/xml')

