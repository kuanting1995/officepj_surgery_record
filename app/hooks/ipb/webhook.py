
from flask import Flask, request, jsonify
import requests,os
from ..route import api_route 
from  settings import Config
from lib.cacheUtils import cache
from lib.Checker import isNationalIdentificationNumberValid, is8Num, is4Num, isNone
from hooks.utils import get_med_info,get_vitalsignData,get_activeorder_all,get_Lab,get_LabDetails,get_translate_gpt
from hooks.ipb.makemsg import makeFlexMsg_PatBaseInfo,makeFlexMsg_OrderDetails,makeFlexMsg_VitalSignChart,makeFlexMsg_Lab,makeFlexMsg_LabDetails
from hooks.ipb.makemsg import makeFlexMsg_List, makeFlexMsg_InPatientDocList,makeFlexMsg_InPatientListByDoc,makeFlexMsg_Translator
from hooks.ipb.utils_teamplus import send_message, sendFlexMsgToUser, upload_image
from hooks.ipb.make_linechart import create_VitalSignChart_main
import uuid
from urllib.parse import parse_qs
from datetime import datetime
from hooks.utils import emrlog,get_user_info_by_ad,sendTextMsgToUser
from lib.logger import logger
from .utils import get_in_patient_doc_list, get_in_patient_by_doc

# demo(IPB):https://ing2.kfsyscc.org/hookap/hooks/ipb/webhook 
# 地端測試(IPB_TEST)：http://172.21.42.22:5000/hookap/hooks/ipb/webhook

# CHANNEL_ACCESS_TOKEN = Config.TEST_IPB_CHANNEL_ACCESS_TOKEN

PRODUCTION = os.getenv('PRODUCTION', "True").strip()

if PRODUCTION in [True, 'true', 'True', 'TRUE']:
    DATABASE_URL = "https://emr.kfsyscc.org/mongo/teamplus_ipb/requests"
    CHANNEL_ACCESS_TOKEN = Config.IPB_CHANNEL_ACCESS_TOKEN
else:
    DATABASE_URL = "https://emr.kfsyscc.org/mongo/teamplus_ipb_test/requests"
    CHANNEL_ACCESS_TOKEN = Config.TEST_IPB_CHANNEL_ACCESS_TOKEN
    

@api_route(rule = '', params=None ,methods=['POST', 'GET'])
def _webhook():
    get_in_patient_by_doc("000834")
    if not request.data:
        emp = get_user_info_by_ad('linhui')
        return "Webhook received!"
    data = request.json
    
    data['empInfo'] = None
    uid = data['events'][0]['source']['userId']
    
    emp = get_user_info_by_ad(uid)
    if(isNone(emp)):
        msg= "未授權的使用者"
        sendTextMsgToUser(uid, msg, CHANNEL_ACCESS_TOKEN) 
        logger.error(msg)
        return msg
    elif (not isNone(emp) and not emp['data']['IS_TOP_ROLE']):
        msg= "您沒有TOP權限，無法查詢"
        sendTextMsgToUser(uid, msg, CHANNEL_ACCESS_TOKEN) 
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
            'ESAM': "檢驗醫囑",
            'CH': "化療",
            'PCA': "PCA",
            'MBD': "出院醫囑",
            '': "全部"
        }
        # postback_handlers為所有按鈕與其對應不同行為
        self.postback_handlers = {
            '1': self.make_vitalsign_handler(),
            '2': self.make_Lab_handler() ,
            '3': self.make_orderbyclass_handler('INJ'),
            '4': self.make_orderbyclass_handler('OP'),
            '5': self.make_orderbyclass_handler('TR'),
            '6': self.make_orderbyclass_handler('ESAM'),
            '7': self.make_orderbyclass_handler('CH'),
            '8': self.make_orderbyclass_handler('PCA'),
            '9': self.make_orderbyclass_handler('MBD'),
            '10': self.make_orderbyclass_handler(''),
            '11': self.make_InPatientDocList_handler(),
            '12': self.make_WriteNote_handler(),
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
            status = cache.get("teampluse:ipb:status:{0}".format(user))
            
            if(req_text.strip().lower() == "list"):
                id =str(uuid.uuid4())
                # msg = makeFlexMsg_List(id)
                # msg = sendFlexMsgToUser(user, msg)
                docs = get_in_patient_doc_list(data['empInfo']['EMP_NO'])
                msg = makeFlexMsg_InPatientDocList(id, docs['data'])
                sendFlexMsgToUser(user, msg)
            elif(req_text.strip().lower() == "mylist"):
                id =str(uuid.uuid4())
                pats = get_in_patient_by_doc(data['empInfo']['EMP_NO'])
                if(isNone(pats) or isNone(pats['data'])):
                    send_message(user, '查無病人資料')
                else:
                    msg = makeFlexMsg_InPatientListByDoc(id, pats['data'], pats['docInfo'])
                    sendFlexMsgToUser(user, msg)
            # 判斷是否為手機/病例號格式
            elif isNationalIdentificationNumberValid(req_text) or is8Num(req_text) or is4Num(req_text):
                try:
                    rs = get_med_info(req_text, data['empInfo']['EMP_NO'])
                    # print('patinfo',rs)
                    obj = rs['data']
                    # 隨機產生uuid碼
                    obj["_id"]=str(uuid.uuid4())
                    _id = obj["_id"]
                    PatBaseInfomsg = makeFlexMsg_PatBaseInfo(_id,obj, data['empInfo']['EMP_NO'])                    
                    msg = sendFlexMsgToUser(user, PatBaseInfomsg)
                    obj["messageSN"] = msg['MessageSN']
                    save_to_db(obj)
                    if(not isNone(rs)):
                        emrlog(data['empInfo']['EMP_NO'], obj['CHART_NO'], 'teampluse_ipb', '住院病人服務頻道,病人資訊查詢')
                except Exception as e:
                    print(str(e))
                    send_message(user, '查無病人資料')
            elif(not isNone(status) and status['status'] == "write_note"):
                _id=str(uuid.uuid4())
                print("req_text", req_text)
                res_text = get_translate_gpt(req_text)
                msg =  makeFlexMsg_Translator(_id, res_text, req_text, status['chartno'], data['empInfo']['EMP_NO'])
                sendFlexMsgToUser(user, msg)
                cache.set("teampluse:ipb:write_note_executed:{0}".format(user), True)
            # 給user的提示操作指令, 病歷創作只能輸入1次, 再次創作要再點1次btn
            elif not status:
                # 確認user 是否執行過 "write_note"
                write_note_executed = cache.get("teampluse:ipb:write_note_executed:{0}".format(user))
                if write_note_executed:
                    send_message(user, "需再次點擊病歷創作")
                # Remove the mark
                    cache.delete("teampluse:ipb:write_note_executed:{0}".format(user))
                else:
                    send_message(user,"資料或格式錯誤,請重新輸入")
            else:
                send_message(user,"資料或格式錯誤,請重新輸入")
            cache.delete("teampluse:ipb:status:{0}".format(user))
    
    # 回覆user點擊btn
    def handle_postback_event(self,data):
        # data={'destination': 2, 'events': [{'type': 'postback', 'timestamp': 1711537555, 'source': {'type': 'user', 'userId': 'clairelu'}, 'data': 'value=0&id=a1e775d4-1594-4a02-8899-e6c958ffa89d'}]}
        user = data['events'][0]['source']['userId']
        qs = data['events'][0]['data']
        print('qs',qs)
        pars = parse_qs(qs)
        postback_data = pars['value'][0]
        _id = pars['id'][0]
        # 點擊btn1,2,3....
        if postback_data in ['1','2','3','4','5','6','7','8','9','10','11','12']: 
            handler = self.postback_handlers.get(postback_data)
            if handler:
                handler(_id,data)
            else:
                send_message(user, '無法判斷btn行為')
        #點擊btn (需病人基本資料obj
        else:
            obj = load_from_db(_id)
            # 從mongo取出postback_handler
            # print('obj', obj)
            postback_handlers = obj['obj']['postback_handlers']
            # print('postback_handlers',postback_handlers)
            self.postback_handlers.update({
                key: self.make_LabDetails_handler(value['category'], value['date'])
                for key, value in postback_handlers.items()
            })
            handler = self.postback_handlers.get(postback_data)
            # print('self.postback_handlers',self.postback_handlers)
            if handler:
                handler(_id, data)
            else:
                send_message(user, '無法判斷btn行為')
            
  
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
     
    # 點擊btn "生命徵象", value ="1", 回傳折線圖
    def make_vitalsign_handler(self):
        def handler(_id,data):
            user = data['events'][0]['source']['userId']
            obj = load_from_db(_id)
            chartno = obj['obj']['CHART_NO']
            patname = obj['obj']['PAT_NAME']
            now = datetime.now().strftime("%Y%m%d")
            print('now',now)
            # 步驟1--api抓取vitalsign數據
            _5days_vitalsignData = get_vitalsignData(chartno,now,7)
            # print('vitalsignData',vitalsignData)
            
            # 步驟2--創建vitalsign折線圖(image_data是binary)
            image_data_main = create_VitalSignChart_main(_5days_vitalsignData)
            
            # 步驟3--上傳 team+ server
            imageid_main = upload_image(image_data_main)
            # print('imageid_main',imageid_main)  imageid_main {'FileID': '7390a1b2-0830-41c6-b06a-54479992eb6c'}
            
            # 步驟4--將image傳送給user
            msg = makeFlexMsg_VitalSignChart(patname,imageid_main)
            sendFlexMsgToUser(user, msg)
            
            
        return handler
    
    
    #點擊btn "檢驗檢查", value="2"
    def make_Lab_handler(self):

        def handler(_id,data):
            user = data['events'][0]['source']['userId']
            obj = load_from_db(_id)
            patname = obj['obj']['PAT_NAME']
            chartno = obj['obj']['CHART_NO']
            # 取最新4筆日期
            lab_data = get_Lab( 5, chartno)
            # lab_data [{'SYS_DATE': '20240430', 'C': '1'}, {'SYS_DATE': '20240429', 'C': '2', 'H': '1'}....]
            # print('lab_data',lab_data)
            # 代出btn選項
            msg = makeFlexMsg_Lab(patname,lab_data,_id)
            # print('msg',msg)
            #根據此病人病檢summary 生出 postback_handlers(從21開始)  ex:'21': self.make_LabDetails_handler('T','20240409)
            postback_handlers = generate_postbackhandler(msg)
            # print('postback_handlers',postback_handlers)
            # 儲存到mongo
            obj['obj']['postback_handlers'] = postback_handlers
            # print('obj',obj)
            update_to_db(obj)
            
            sendFlexMsgToUser(user, msg)
            
        
        # obj['obj']['postback_handlers']= {
        #     "21": {
        #         "category": "C",
        #         "date": "20240514"
        #     },...}
        def generate_postbackhandler(data):
            result = {}
            for container in data['contents']['footer']:
                if container['type'] == 'footercontainer':
                    for content in container['contents']:
                        if content['type'] == 'postbackbutton':
                            info = content['data'].split('&')
                            value = int(info[0].split('=')[1])
                            category = info[2].split('=')[1]
                            date = info[3].split('=')[1]
                            result[value] = {'category': category, 'date': date}
                            
            return result
    
            
        return handler
        
    
    # 點擊btn "檢驗檢查分類"=> 產出表格details
    def make_LabDetails_handler(self,category,date):
        def handler(_id, data):
            user = data['events'][0]['source']['userId']
            obj = load_from_db(_id)
            patname = obj['obj']['PAT_NAME']
            chartno = obj['obj']['CHART_NO']
            # lab_details = get_LabDetails('06632459', 'H', '20240503')
            lab_details = get_LabDetails(chartno, category, date)
            # print('lab_details',lab_details)
            if(isNone(lab_details)):
                send_message(user, '查無資料')
            else:
                msg = makeFlexMsg_LabDetails(patname, category, lab_details)
                # msg = make_test()
                # print('msg',msg)
                sendFlexMsgToUser(user, msg)
            
        return handler
    
    #點擊btn "主治醫師病人清單", value="11"
    def make_InPatientDocList_handler(self):

        def handler(_id, data):
            user = data['events'][0]['source']['userId']
            id=str(uuid.uuid4())
            qs = data['events'][0]['data']
            pars = parse_qs(qs)
            api = pars['api'][0]
            if(api == "in_patient_doc_list"):
                docs = get_in_patient_doc_list(data['empInfo']['EMP_NO'])
                msg = makeFlexMsg_InPatientDocList(id, docs['data'])
                sendFlexMsgToUser(user, msg)
            elif(api == "in_patient_list_by_doc"):
                docno = pars['docno'][0]
                pats = get_in_patient_by_doc(docno)
                # print("pats['data']",pats['data'])
                msg = makeFlexMsg_InPatientListByDoc(id, pats['data'], pats['docInfo'])
                sendFlexMsgToUser(user, msg)
            elif(api == "in_patient_info"):
                cahrtno = pars['cahrtno'][0]
                try:
                    rs = get_med_info(cahrtno, data['empInfo']['EMP_NO'])
                    # print('patinfo',rs)
                    obj = rs['data']
                    # 隨機產生uuid碼
                    obj["_id"]=str(uuid.uuid4())
                    _id = obj["_id"]
                    PatBaseInfomsg = makeFlexMsg_PatBaseInfo(_id,obj, data['empInfo']['EMP_NO'])                    
                    msg = sendFlexMsgToUser(user, PatBaseInfomsg)
                    obj["messageSN"] = msg['MessageSN']
                    save_to_db(obj)
                    if(not isNone(rs)):
                        emrlog(data['empInfo']['EMP_NO'], obj['CHART_NO'], 'teampluse_ipb', '住院病人服務頻道,病人資訊查詢')
                except Exception as e:
                    print(str(e))
                    send_message(user, '查無病人資料')                
            else:
                send_message(user, '查無資料')
        return handler    

    #點擊btn "病例創作", value="12"
    def make_WriteNote_handler(self):

        def handler(_id, data):
            user = data['events'][0]['source']['userId']
            id=str(uuid.uuid4())
            qs = data['events'][0]['data']
            pars = parse_qs(qs)
            api = pars['api'][0]
            if(api == "write_note"):
                chartno = pars['chartno'][0]
                cache.set("teampluse:ipb:status:{0}".format(user), {"status":"write_note", "chartno":chartno}, timeout=600)
            else:
                send_message(user, '查無資料')
        return handler   
    
bot = ChatBotFSM()


#儲存資料至mongodb: https://emr.kfsyscc.org/madmin/db/teamplus_ipb/
def save_to_db(obj):
    url = DATABASE_URL
    payload = {
        "progress_name": "住院病人資訊",
        "messageSN": obj["messageSN"],
        "obj":obj,
        "_id": obj["_id"]
    }
    x = requests.post(url, json=payload)
    # print(x.text)
    
def load_from_db(a_id):
    url = DATABASE_URL + "/" + a_id
    x = requests.get(url)
    return x.json()

def update_to_db(obj):
    url = DATABASE_URL + "/" + obj["_id"]
    x = requests.put(url, json=obj)
    # print(x.text)