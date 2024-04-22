
from flask import Flask, request, jsonify
import requests
from ..route import api_route 
from  settings import Config
from lib.Checker import isNationalIdentificationNumberValid, is8Num, is4Num, isNone
from hooks.utils import get_med_info,get_vitalsignData,get_activeorder_all, get_user_info_by_ad
from hooks.ipb.makemsg import makeFlexMsg_PatBaseInfo, makeFlexMsg_CategoryOrder,makeFlexMsg_OrderDetails,makeFlexMsg_VitalSignChart
from hooks.ipb.utils_teamplus import send_message, sendFlexMsgToUser, upload_image
from hooks.ipb.make_linechart import create_VitalSignChart
import uuid
from urllib.parse import parse_qs
from datetime import datetime
from lib.logger import logger


# demo:https://ing2.kfsyscc.org/hookap/hooks/ipb/webhook 
# 地端測試：http://172.21.42.22:5001/hookap/hooks/ipb/webhook

CHANNEL_ACCESS_TOKEN = Config.IPB_CHANNEL_ACCESS_TOKEN

@api_route(rule = '', params=None ,methods=['POST', 'GET'])
def _webhook():
    if not request.data:
        return "Webhook received!"
    
    data = request.json
    data['empInfo'] = None
    uid = data['events'][0]['source']['userId']
    
    emp = get_user_info_by_ad(uid)
    if(isNone(emp) or (not emp['status']) or isNone(emp['data']) ):
        msg= "未授權的使用者"
        send_message(uid, msg) 
        logger.error(msg)
        return msg
    else:
        data['empInfo'] = emp['data']

        
        
    bot.handle_event(data['events'][0]['type'], data)
    return data

# 聊天訊息處理
class ChatBotFSM:
    def __init__(self):
        self.order_type_dict = {
            'INJ': "點滴/針劑",
            'OP': "口服/外用",
            'TR': "醫療指示",
            'ESAM': "檢驗檢查",
            'CH': "化療",
            'PCA': "PCA",
            'MBD': "出院醫囑",
            '': "全部"
        }
        # postback_handlers為所有按鈕與其對應不同行為
        self.postback_handlers = {
            '0': self.make_postback_handler(makeFlexMsg_CategoryOrder),
            '1': self.make_vitalsign_handler(),
            '3': self.make_orderbyclass_handler('INJ'),
            '4': self.make_orderbyclass_handler('OP'),
            '5': self.make_orderbyclass_handler('TR'),
            '6': self.make_orderbyclass_handler('ESAM'),
            '7': self.make_orderbyclass_handler('CH'),
            '8': self.make_orderbyclass_handler('PCA'),
            '9': self.make_orderbyclass_handler('MBD'),
            '10': self.make_orderbyclass_handler(''),
        }
    # 判斷事件類型並執行自動回覆：user輸入文字訊息=>message,user點擊btn=>postback
    def handle_event(self, event_type, data):
        if event_type == 'message':
            self.handle_message_event(data)
        elif event_type == 'postback':
            self.handle_postback_event(data)
    # 回覆user的文字訊息
    def handle_message_event(self, data):
            req_text = data['events'][0]['message']['text'] 
            user = data['events'][0]['source']['userId']
            emp =  data['empInfo']
            # 判斷是否為手機/病例號格式
            if isNationalIdentificationNumberValid(req_text) or is8Num(req_text) or is4Num(req_text):
                try:
                    rs = get_med_info(req_text, emp['EMP_NO'])
                    # print('patinfo',rs)
                    obj = rs['data']
                    # 隨機產生uuid碼
                    obj["_id"]=str(uuid.uuid4())
                    _id = obj["_id"]
                    PatBaseInfomsg = makeFlexMsg_PatBaseInfo(_id,obj)
                    msg = sendFlexMsgToUser(user, PatBaseInfomsg)

                    obj["messageSN"] = msg['MessageSN']
                    save_to_db(obj)
                except Exception as e:
                    print(str(e))
                    send_message(user, '查無病人資料')
            else:
                send_message(user,"資料或格式錯誤,請重新輸入")
    
    # 回覆user點擊btn
    def handle_postback_event(self,data):
        # data={'destination': 2, 'events': [{'type': 'postback', 'timestamp': 1711537555, 'source': {'type': 'user', 'userId': 'clairelu'}, 'data': 'value=0&id=a1e775d4-1594-4a02-8899-e6c958ffa89d'}]}
        user = data['events'][0]['source']['userId']
        qs = data['events'][0]['data']
        print('qs',qs)
        pars = parse_qs(qs)
        postback_data = pars['value'][0]
        _id = pars['id'][0]
        if postback_data == '0':
            handler = self.postback_handlers.get(postback_data)
            if handler:
                handler(_id,data)
            else:
                send_message(user, '無法判斷btn行為')
        elif postback_data == '20':
            handler = self.postback_handlers.get(postback_data)
            if handler:
                handler(_id,data)
            else:
                send_message(user, '無法判斷btn行為')
        elif postback_data == '1':
            handler =self.postback_handlers.get(postback_data)
            if handler:
                handler(_id,data)
            else:
                send_message(user, '無法判斷btn行為')
        #點擊btn1~12, 產生btn (value1~12的執行：postback_handlers)  ex:'1': self.make_orderbyclass_handler('口服')
        else:
            obj = load_from_db(_id)
            handler = self.postback_handlers.get(postback_data)
            if handler:
                handler(_id, data)
            else:
                send_message(user, '無法判斷btn行為')
            
    # 點擊btn0後行為,製作msg(病人基本資料+3btn):flexmsg,並傳送flex:handler()
    def make_postback_handler(self,flexmsg):
        def handler(_id,data):
            obj = load_from_db(_id)
            user = data['events'][0]['source']['userId']
            # print('obj',obj)
            sendFlexMsgToUser(user, flexmsg(_id,obj))
        return handler
    
    # 點擊btn3~10後行為,製作orderdetails
    def make_orderbyclass_handler(self, ordertype):
        def handler(_id,data):
            user = data['events'][0]['source']['userId']
            obj = load_from_db(_id)
            chartno = obj['obj']['CHART_NO']
            inpno = obj['obj']['INP_NO']
            patname = obj['obj']['PAT_NAME']
            bedno = obj['obj']['NOW_BEDNO']
            # print('last msg',obj)
            # 獲取ordertype對應中文值：
            ordertype_value = self.order_type_dict.get(ordertype,ordertype)
            rs = get_activeorder_all(chartno,inpno,ordertype)
            order_data = rs['data']
            # print('order data',order_data)
            if not order_data:
                send_message(user, "此active order分類尚無資料")
                return 
            else:
                msg = makeFlexMsg_OrderDetails(patname,bedno,ordertype_value ,order_data)
                # print('msg', msg)
                sendFlexMsgToUser(user, msg)

        return handler  
     
    # 點擊btn1 回傳病人生命徵象折線圖
    def make_vitalsign_handler(self):
        def handler(_id,data):
            user = data['events'][0]['source']['userId']
            emp =  data['empInfo']
            obj = load_from_db(_id)
            chartno = obj['obj']['CHART_NO']
            patname = obj['obj']['PAT_NAME']
            now = datetime.now().strftime("%Y%m%d")
            print('now',now)
            # -api抓取vitalsign數據
            _5days_vitalsignData = get_vitalsignData(chartno,now,7)
            # print('vitalsignData',vitalsignData)
            
            # -創建vitalsign折線圖(image_data是binary)
            image_data = create_VitalSignChart(_5days_vitalsignData)
            # print('image_data',image_data)

            # -上傳 team+ server
            imageid = upload_image(image_data)
            # print('imageid',imageid)  imageid {'FileID': '7390a1b2-0830-41c6-b06a-54479992eb6c'}
            
            # -將image傳送給user
            msg = makeFlexMsg_VitalSignChart(patname,imageid)
            sendFlexMsgToUser(user, msg)
            
            
        return handler
    
bot = ChatBotFSM()


#儲存資料至mongodb: https://emr.kfsyscc.org/madmin/db/teamplus_ipb/
def save_to_db(obj):

    url = "https://emr.kfsyscc.org/mongo/teamplus_ipb/requests"
    payload = {
        "progress_name": "住院病人資訊",
        "messageSN": obj["messageSN"],
        "obj":obj,
        "_id": obj["_id"]
    }
    x = requests.post(url, json=payload)
    
    
def load_from_db(a_id):
    url = "https://emr.kfsyscc.org/mongo/teamplus_ipb/requests/" + a_id
    x = requests.get(url)
    return x.json()
