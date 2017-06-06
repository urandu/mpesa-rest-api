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
    parse_confirmation_request, parse_confirmation_response
from mpesa import settings


@csrf_exempt
def index(request):

    payload = \
        {
            "result_code": "badam",
            "result_description": "ssss",
            "custom_trans_id": "ssss"
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

            xml_response = parse_confirmation_response(response.content)

            return HttpResponse(xml_response, content_type='application/xml')
