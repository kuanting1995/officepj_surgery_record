
from flask import Flask, request, jsonify
from ..route import api_route
from datetime import datetime  
import requests

 

CHANNEL_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cGUiOiJKV1QifQ.eyJ0eXBlIjowLCJleHAiOjAsImlkIjoxMX0.wNMeUbhzFevFS6c5FxlUW7Hjzb4e5iDlwWCJYivPq5A"


@api_route(rule = '', params=None ,methods=['POST', 'GET'])
def _webhook():
    '''{ "Description": "webhook", "Methods":"POST", "Content-Type":"application/json",
         "Parameters":[
         ]
    }'''    
    
    if not request.data: # for team+ verification
        return "Webhook received!"
    data = request.json
    user_account = data['events'][0]['source']['userId']
    print('critical_confirm_webhook:', data)

    event_type = data['events'][0]['type']
    return data

     