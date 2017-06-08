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
    parse_checkout_request_body, parse_checkout_response
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

        response = requests.post(url, data=payload)

        response = parse_checkout_response(response)

        #
        # if response.ok:
        #
        #     xml_response = parse_confirmation_response()
        #
        #     return HttpResponse(xml_response, content_type='application/xml')
