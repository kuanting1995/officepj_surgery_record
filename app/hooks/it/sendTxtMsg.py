
import requests
import json
from lib.utils import api_response
from ..route import api_route
from datetime import datetime   
from lib.cacheUtils import cache
from  settings import Config
from lib.utils import call_api
from lib.logger import logger
from lib.Checker import isNone

CHANNEL_ACCESS_TOKEN = Config.IT_CHANNEL_ACCESS_TOKEN

req_params = {}
req_params['UserID'] = ['required']
req_params['TextMsg'] = ['required']


@api_route(rule = '', params=req_params ,methods=['POST', 'GET'])
def _sendTxtMsg(args):
    '''{ "Description": "HelloWorld", "Methods":"POST, GET", "Content-Type":"application/json",
         "Parameters":[
             {"Description":"UserID", "Name":"UserID", "Required":true},
             {"Description":"TextMsg", "Name":"TextMsg", "Required":true}

         ]
    }'''    
    
    response_data = {}

    def _check_parameter():
        args['now'] = datetime.now()
        args['USER_INFO'] = get_user_info(args['UserID'])
        if(isNone(args['USER_INFO']) or not args['USER_INFO']['status']):
            raise Exception('員工資料錯誤')
        
    def _deal():
        pass
    
    def _responseData():
        response_data['status'] = True
        response_data['message'] =  ''
        response_data['data'] = send_message(args['USER_INFO']['data']['AD_ACCOUNT'].lower(), args['TextMsg'])

        return response_data
    try:
        _check_parameter()
        _deal() 
        return api_response(_responseData()), 200
    except Exception as e:
        rs = {'status':False, 'message': str(e), 'data': None}  
        return api_response(rs), 400
    finally:
        pass
            
 

@cache.memoize(10)  
def send_message(recipient, message):
    url = "https://eim.kfsyscc.org/API/MessageFeedService.ashx"

    # 簡易版通知（team+ 需開啟一對一交談）
    payload = {
        "ask": "sendMessage",
        "recipient": recipient,
        "message": {"type": "text", "text": message},
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": CHANNEL_ACCESS_TOKEN,
    }

    x = requests.post(url, headers=headers, json=payload)
    return x.json()

@cache.memoize(3600)  
def get_user_info(user_id):
    rs = None
    try:
        URI = "{0}/slight/api/emp/CurrentEmployee".format(Config.K8S_URL)
        # 資料
        req_data = {
            "EMP_NO": user_id,
            "USER_ID": "KFSYSCC"
        }
        headers={ 'Content-Type': 'application/json'}
        content = call_api(uri= URI, payload= json.dumps(req_data), headers= headers, timeout=10)
        if(not isNone(content) ):
            rs = json.loads(content)
    except Exception as e: 
        logger.error('get_user_info: {0}'.format(str(e))) 
        return None
    return rs

