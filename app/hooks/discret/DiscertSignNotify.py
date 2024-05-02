
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
req_params['CertNo'] = ['required']


@api_route(rule = '', params=req_params ,methods=['POST', 'GET'])
# @apikey_required(apifor=['KFSYSCC'])
def _sendDiscertSignNotify(args):
    '''{ "Description": "傳送診斷書簽署通知", "Methods":"POST, GET", "Content-Type":"application/json",
         "Parameters":[
             {"Description":"UserID (DocNo)", "Name":"UserID", "Required":true},
             {"Description":"CertNo", "Name":"CertNo", "Required":true}

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
        cert = get_DiagCertificate(args['USER_INFO']['EMP_NO'], args['CertNo'])
        if(not isNone(cert)):
            cert[0]['_id']  = str(uuid.uuid4())
            msg = makeFlexMsg(cert[0])
            if(Config.APP_MODE != 'PRODUCTION'):
                teamApiResult = sendFlexMsgToUser('linhui', msg,  CHANNEL_ACCESS_TOKEN)
                teamApiResult = sendFlexMsgToUser('butterfly', msg,  CHANNEL_ACCESS_TOKEN)
                teamApiResult = sendFlexMsgToUser('jerry06111', msg,  CHANNEL_ACCESS_TOKEN)
            else:
                teamApiResult = sendFlexMsgToUser(args['USER_INFO']['AD_ACCOUNT'].lower(), msg,  CHANNEL_ACCESS_TOKEN)
          		

            
            response_data['data'] = teamApiResult
            response_data['status'] = False if("MessageSN" not in teamApiResult) else True
            response_data['message'] = teamApiResult['MessageSN'] if('MessageSN' in teamApiResult) else teamApiResult['message']
            msgSN = teamApiResult["MessageSN"]
            cert[0]["messageSN"] = msgSN
            save_to_db(cert[0], "乙種診斷書")
            
  
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


def get_DiagCertificate(docno, certno):
    rs = None
    try:
        URI = "{0}/emrap/api/Discret/GetDiagCertificate".format(Config.K8S2_URL)
        req_data = {
            "DOC_NO": docno,
            "CERT_NO": certno
        }
        headers={ 'Content-Type': 'application/json'}
        content = call_api(uri= URI, payload= json.dumps(req_data), headers= headers, timeout=15)
        if(not isNone(content) ):
            rs = json.loads(content)
    except Exception as e:
        logger.error('get_DiagCertificate: {0}'.format(str(e))) 
        return None
    return rs['data']


def makeFlexMsg(data):
    if(isNone(data['CERT_NO']) or isNone(data['DOC_NO'])):
        raise ValueError("資料錯誤")
    
    id = data['_id']
    certno = data['CERT_NO']
    patname = data['PAT_NAME']
    chartno = data['CHART_NO']
    memoICD = data['MEMO_ICD']
    memoPlan = data['MEMO_PLAN']
    docNo = data['DOC_NO']
    userName= data['USER_NAME']
    
    
    cretDate = None
    try:
        cretDate = datetime.strptime(data['CERT_DATE'], "%Y%m%d")
        cretDate = datetime.strftime(cretDate, "%Y/%m/%d")
    except Exception as e:
        cretDate = " "

    


    msg = {
	"type": "flex",
	"contents": {
		"body": [
			{
				"type": "bodycontainer",
				"contents": [
					{
						"type": "text",
						"text": "乙種診斷證明書簽署",
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 18,
						"fontStyle": "normal",
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
						"text": "{0}-{1}".format(patname, chartno),
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontStyle": "normal",
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
						"text": "編號",
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 14,
						"fontStyle": "normal",
						"fontWeight": 400,
						"marginTop": 10
					},
					{
						"type": "text",
						"text": certno,
						"flex": 5,
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontStyle": "normal",
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
						"fontStyle": "normal",
						"fontWeight": 400,
						"marginTop": 10
					},
					{
						"type": "text",
						"text": cretDate,
						"flex": 5,
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontStyle": "normal",
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
						"text": "開單",
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontStyle": "normal",
						"fontWeight": 400,
						"marginTop": 10
					},
					{
						"type": "text",
						"text": userName,
						"flex": 5,
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontStyle": "normal",
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
						"text": "診斷",
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontStyle": "normal",
						"fontWeight": 400,
						"marginTop": 10
					},
					{
						"type": "text",
						"text": memoICD,
						"flex": 5,
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontStyle": "normal",
						"fontWeight": 400,
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
						"text": memoPlan,
						"align": "left",
						"fontColor": "#ff0000",
						"fontSize": 14,
						"fontStyle": "normal",
						"fontWeight": 400,
						"marginTop": 10
					}
				],
				"borderColor": "#DCDCDC",
				"paddingTop": 0,
				"paddingBottom": 0,
				"paddingStart": 10,
				"paddingEnd": 10
			}   
		],
		"footer": [
			{
				"type": "footercontainer",
				"contents": [
					{
                        "id": "{0}-comfirm".format(id),
						"type": "postbackbutton",
						"text": "確認",
						"style": "primary",
						"displayText": "確認中...",
						"data": "api=comfirm-discert&msgid={0}&docno={1}&certno={2}".format(id, docNo, certno)
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
                      "id": "{0}-preview".format(id),
						"type": "postbackbutton",
						"text": "瀏覽",
						"style": "primary",
						"displayText": "產生畫面中...",
						"data": "api=preview-discert&msgid={0}&docno={1}&certno={2}".format(id, docNo, certno)
					}
				],
				"borderColor": "#DCDCDC",
				"paddingTop": 0,
				"paddingBottom": 0,
				"paddingStart": 10,
				"paddingEnd": 10
			},   
			{
				"type": "footercontainer",
				"contents": [
					{
                        "id": "{0}-delete".format(id),
						"type": "postbackbutton",
						"text": "刪除",
						"style": "secondary",
						"displayText": "刪除中...",
						"data": "api=delete-discert&msgid={0}&docno={1}&certno={2}".format(id, docNo, certno)
    				}
				],
				"borderColor": "#DCDCDC",
				"paddingStart": 10,
				"paddingEnd": 10
			},

		]
	}
}
    return msg

# 生命徵象折線圖
def makeFlexMsg_DecertPreview(patname, imageid):
    
    msg = {
	"type": "flex",
	"contents": {
		"body": [
			{
				"type": "bodycontainer",
				"contents": [
					{
						"type": "text",
						"text": f"病人{patname} 診斷書",
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 16,
						"fontStyle": "normal",
						"fontWeight": 900,
						"marginTop": 5
					}
				],
				"borderColor": "#DCDCDC",
				"paddingBottom": 20,
				"paddingStart": 10,
				"paddingEnd": 10
			},
			{
				"type": "bodycontainer",
				"contents": [
					{
						"type": "image",
						"id": imageid['FileID'],
						"aspectRatio": "7:3",
						"scaleType": "fit"
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