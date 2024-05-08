
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
from hooks.utils import get_user_info
from lib.web import  apikey_required
from hooks.utils import sendFlexMsgToUser
from .utils import save_to_db, CHANNEL_ACCESS_TOKEN
import uuid


req_params = {}
req_params['UserID'] = ['required']



@api_route(rule = '', params=req_params ,methods=['POST', 'GET'])
# @apikey_required(apifor=['KFSYSCC'])
def _ColorTest(args):
    '''{ "Description": "測試", "Methods":"POST, GET", "Content-Type":"application/json",
         "Parameters":[
             {"Description":"UserID", "Name":"UserID", "Required":true}

         ]
    }'''    
    
    response_data = {}

    def _check_parameter():
        args['now'] = datetime.now()
        args['USER_INFO'] = get_user_info(args['UserID'])
        if(isNone(args['USER_INFO']) or not args['USER_INFO']['status']):
            raise Exception('員工資料錯誤')
        else:
            args['USER_INFO'] = args['USER_INFO']['data']
        
    def _deal():
        pass
    
    def _responseData():
        response_data['status'] = False
        response_data['message'] =  ''
        response_data['data'] = None

        msg = makeFlexMsg()
        teamApiResult = sendFlexMsgToUser(args['USER_INFO']['AD_ACCOUNT'].lower(), msg,  CHANNEL_ACCESS_TOKEN)
          		
  
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





def makeFlexMsg():
    msg = {
	"type": "flex",
	"contents": {
		"body": [
			{
				"type": "bodycontainer",
				"contents": [
					{
						"type": "text",
						"text": "視訊會議新方案介紹",
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 18,
						"fontWeight": 900,
						"marginTop": 10
					}
				],
				"borderColor": "#DCDCDC",
				"paddingStart": 10,
				"paddingEnd": 10
			},
			{
				"type": "bodycontainer",
				"contents": [
					{
						"type": "text",
						"text": "業務、行銷其他有需求人員皆可自由參加",
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontWeight": 900,
						"marginTop": 10
					}
				],
				"borderColor": "#DCDCDC",
				"paddingStart": 10,
				"paddingEnd": 10
			},
			{
				"type": "separator",
				"height": 1,
				"bgcolor": "#DCDCDC"
			},
			{
				"type": "bodycontainer",
				"contents": [
					{
						"type": "text",
						"text": "地點",
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontWeight": 400,
						"marginTop": 10
					},
					{
						"type": "text",
						"text": "會議室 - A",
						"flex": 5,
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontWeight": 400,
						"marginTop": 10
					}
				],
				"borderColor": "#DCDCDC",
				"paddingStart": 10,
				"paddingEnd": 10
			},
			{
				"type": "bodycontainer",
				"contents": [
					{
						"type": "text",
						"text": "日期",
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontWeight": 400,
						"marginTop": 10
					},
					{
						"type": "text",
						"text": "2020-07-04 (六)",
						"flex": 5,
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontWeight": 400,
						"marginTop": 10
					}
				],
				"borderColor": "#DCDCDC",
				"paddingStart": 10,
				"paddingEnd": 10
			},
			{
				"type": "bodycontainer",
				"contents": [
					{
						"type": "text",
						"text": "時間",
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontWeight": 400,
						"marginTop": 10
					},
					{
						"type": "text",
						"text": "09:15 ~ 15:30",
						"flex": 5,
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontWeight": 400,
						"marginTop": 10
					}
				],
				"borderColor": "#DCDCDC",
				"paddingStart": 10,
				"paddingEnd": 10
			}
		],
		"footer": [
			{
				"type": "footercontainer",
				"contents": [
					{
						"type": "messagebutton",
						"text": "Message Button",
						"style": "primary",
						"fontColor": "#000000",
						"bgcolor": "#F34A4A",      
      					"message": "test"
					}
				],
				"borderColor": "#DCDCDC",
				"paddingStart": 10,
				"paddingEnd": 10
			},
			{
				"type": "footercontainer",
				"contents": [
					{
						"type": "messagebutton",
						"text": "Message Button",
						"style": "secondary",
						"message": "test"
					}
				],
				"borderColor": "#DCDCDC",
				"paddingStart": 10,
				"paddingEnd": 10
			}
		]
	}
}
    return msg