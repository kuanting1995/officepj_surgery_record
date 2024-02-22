
from flask import Flask, request, jsonify
from ..route import api_route
from datetime import datetime  
from  settings import Config

 

CHANNEL_ACCESS_TOKEN = Config.IT_CHANNEL_ACCESS_TOKEN


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

     