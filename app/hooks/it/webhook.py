
from flask import Flask, request, jsonify
import requests
import json
from ..route import api_route 
from  settings import Config
from lib.Checker import isNationalIdentificationNumberValid, is8Num, is4Num
from hooks.utils import get_med_info,get_activeorder_all,get_activeorder_byClass
from hooks.makemsg import makeFlexMsg_PatBaseInfo, makeFlexMsg_CategoryOrder,makeFlexMsg_OrderDetails
from hooks.utils_teamplus import send_message, sendFlexMsgToUser ,updateFlexFooter
# demo:https://ing2.kfsyscc.org/hookap/hooks/it/webhook 
# 地端測試：http://172.21.42.22:5000/hookap/hooks/it/webhook

CHANNEL_ACCESS_TOKEN = Config.IT_CHANNEL_ACCESS_TOKEN

@api_route(rule = '', params=None ,methods=['POST', 'GET'])
def _webhook():
    if not request.data:
        return "Webhook received!"
    data = request.json
    bot.handle_event(data['events'][0]['type'], data)
    return data

# 聊天訊息處理
class ChatBotFSM:
    def __init__(self):
        self.state = 'waiting_for_user_input'
        self.user = None
        self.pat_baseinfo = None
        self.message_sn = None
        self.chartno = None
        # postback_handlers為所有按鈕與其對應不同行為
        self.postback_handlers = {
            'value=0': self.make_postback_handler(get_activeorder_all, makeFlexMsg_CategoryOrder),
            'value=3': self.make_orderbyclass_handler('0'),
            'value=4': self.make_orderbyclass_handler('00'),
            'value=5': self.make_orderbyclass_handler('02'),
            'value=6': self.make_orderbyclass_handler('03'),
            'value=7': self.make_orderbyclass_handler('04')
        }
    # 判斷事件類型並執行自動回覆：user輸入文字訊息=>message,user點擊btn=>postback
    def handle_event(self, event_type, data):
        if event_type == 'message':
            self.handle_message_event(data)
        elif event_type == 'postback':
            self.handle_postback_event(data)
    # 回覆user的文字訊息
    def handle_message_event(self, data):
        if self.state == 'waiting_for_user_input':
            req_text = data['events'][0]['message']['text'] 
            self.user = data['events'][0]['source']['userId']
            # 判斷是否為手機/病例號格式
            if isNationalIdentificationNumberValid(req_text) or is8Num(req_text) or is4Num(req_text):
                try:
                    rs = get_med_info(req_text)
                    self.pat_baseinfo = rs['data']
                    print('self_baseinfo',self.pat_baseinfo)
                    data = self.pat_baseinfo
                    msg = sendFlexMsgToUser(self.user, makeFlexMsg_PatBaseInfo(data))
                    self.message_sn = msg['MessageSN']
                except Exception as e:
                    print(str(e))
                    send_message(self.user, '查無病人資料')
            else:
                send_message(self.user,"資料或格式錯誤,請重新輸入")
    # 回覆user點擊btn 
    def handle_postback_event(self, data):
        postback_data = data['events'][0]['data']
        # data= {'destination': 2, 'events': [{'type': 'postback', 'timestamp': 1710513322, 'source': {'type': 'user', 'userId': 'clairelu'}, 'data': 'value=0'}]}
        # 判斷user按下哪顆按鈕=> postback_data :value=3 , 對應按鈕的行為=>handler:make_orderbyclass_handler('0')
        handler = self.postback_handlers.get(postback_data)
        if handler:
            handler(data)
        else:
            send_message(self.user, '無法判斷btn行為')
            
    # 點擊btn後行為(共用),獲得資料get_data,製作msg:flexmsg,並傳送flex:handler()
    def make_postback_handler(self, get_data, flexmsg):
        def handler(data):
            pat_baseinfo = self.pat_baseinfo
            if pat_baseinfo:
                chartno = pat_baseinfo['CHART_NO']
                self.chartno = chartno
                print('chartno', chartno)
                data.update(get_data(chartno))  # Pass chartno to get_data function
                data['PAT_BASEINFO']= pat_baseinfo
                # print('dataa', data)
            else:
                print("pat_baseinfo is None or does not contain 'PAT_NAME'")
            sendFlexMsgToUser(self.user, flexmsg(data))
        return handler  

    def make_orderbyclass_handler(self, majorclass):
        def handler(data):
            pat_baseinfo = self.pat_baseinfo
            chartno = self.chartno
            ddl = get_activeorder_all(chartno)
            data = get_activeorder_byClass(majorclass,ddl)
            # print(pat_baseinfo)
            data['PAT_INFO']=pat_baseinfo
            # print(data)
            if not data or not 'data' in data or not data['data']:
                send_message(self.user, "此active order分類尚無資料")
                return 
            else:
                # Make and send message
                msg = makeFlexMsg_OrderDetails(data)
                # print('msg', msg)
                sendFlexMsgToUser(self.user, msg)

        return handler  # Add this line

bot = ChatBotFSM()

