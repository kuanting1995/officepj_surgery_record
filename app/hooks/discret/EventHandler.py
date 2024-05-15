
from flask import Flask, request, jsonify
import requests
from ..route import api_route 
import json
from  settings import Config
from lib.Checker import isNationalIdentificationNumberValid, is8Num, is4Num, isNone
from hooks.utils import sendFlexMsgToUser, sendTextMsgToUser, upload_image
from lib.utils import call_api_default
from urllib.parse import parse_qs
from datetime import datetime
from lib.logger import logger
from .utils import load_from_db
import inspect
from lib.utils import TLSAdapter

# 聊天訊息處理
class BotEventHandler:
    
    def __init__(self, accesstoken):
    
        # postback_handlers為所有按鈕與其對應不同行為
        self.AccessToken = accesstoken
        self.postback_handlers = {
            'comfirm-discert': comfirm_discert,
            'preview-discert': preview_discert,
            'delete-discert': delete_discert,
            
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
 
    
    # 回覆user點擊btn
    def handle_postback_event(self, data):
        user = data['events'][0]['source']['userId']
        qs = data['events'][0]['data']
        pars = parse_qs(qs)
        api = pars['api'][0]
        if(api in self.postback_handlers ):
            handle = self.postback_handlers[api]
            if(inspect.isfunction(handle)):
                handle(self, data)
        else:
            sendTextMsgToUser(user, '無法判斷btn行為', self.AccessToken )
 
from .DiscertSignNotify import get_DiagCertificate, makeFlexMsg_DecertPreview

def is_overtime(dtimestamp):
    now = datetime.now()
    ts = now.timestamp()  
    time_difference_seconds = ts - dtimestamp
    # 将秒转换为更容易理解的格式
    hours = time_difference_seconds // 3600
    minutes = (time_difference_seconds % 3600) // 60
    seconds = time_difference_seconds % 60
    print(f"Time difference: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds") 
    return hours>=24


def request_api(url):
    import requests
    try:
        
        requests.adapters.DEFAULT_RETRIES = 3 #重連次數 
        s = requests.session()
        try:
            isHttps = url.index('https://')
            if(isHttps == 0):
                s.mount('https://', TLSAdapter())
        except Exception as e:
            logger.info('call_api_get_mount:{0}'.format(str(e)))

        s.keep_alive = False # 關閉多餘連結
        response = s.get(url)
        response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx or 5xx)

        # Try to get encoding from headers if specified
        encoding = response.encoding if response.encoding != 'ISO-8859-1' else None  # Requests assumes ISO-8859-1 if encoding is not specified
        # If no encoding is found in headers, you may need to guess or manually set it
        if not encoding:
            encoding = 'big5'  # This is a common encoding for traditional Chinese content, which might be the case here
        # Decode the content with the correct encoding
        content = response.content.decode(encoding)
        return content  # Now `content` should be a properly decoded string

    except requests.RequestException as e:
        print(f"Request failed: {e}")
    except UnicodeDecodeError as e:
        print(f"Decoding failed: {e}")

   
def comfirm_discert(caller, data):
   
    now = datetime.now()
    ts = now.timestamp()
    user = data['events'][0]['source']['userId']
    emp =  data['empInfo']
    qs = data['events'][0]['data']
    pars = parse_qs(qs)
    msgid = pars['msgid'][0]  if('msgid'in pars) else   None
    docno = pars['docno'][0]  if('docno'in pars) else   None
    certno = pars['certno'][0]  if('certno'in pars) else   None
     
    if(isNone(msgid)):
        sendTextMsgToUser(user, '訊息已過期', caller.AccessToken)
        return False
    msg = load_from_db(msgid)
    
    
    if(isNone(msg) or is_overtime(msg['req_datetime'])):
        sendTextMsgToUser(user, '訊息已過期', caller.AccessToken)
        return False
    

    cert = get_DiagCertificate(docno, certno)
    if(not isNone(cert) and not isNone(cert[0]['CONFIRM_URL']) and cert[0]['DOC_NO'] == emp['EMP_NO']):
        request_api(cert[0]['CONFIRM_URL'])
        logger.info("{0}-{1}".format(emp['EMP_NO'], '診斷書已確認'))
        sendTextMsgToUser(user, '{0}-診斷書已確認'.format(msg['rawdata']['PAT_NAME']), caller.AccessToken)
    elif(not isNone(cert) and cert[0]['DOC_NO'] != emp['EMP_NO']):
        sendTextMsgToUser(user, '人員身份認證錯誤無法簽章', caller.AccessToken)
    else:
        sendTextMsgToUser(user, '{0}-診斷書已確認!'.format(msg['rawdata']['PAT_NAME']), caller.AccessToken)

def delete_discert(caller, data):
    now = datetime.now()
    ts = now.timestamp()
    user = data['events'][0]['source']['userId']
    emp =  data['empInfo']
    qs = data['events'][0]['data']
    pars = parse_qs(qs)
    msgid = pars['msgid'][0]  if('msgid'in pars) else   None
    docno = pars['docno'][0]  if('docno'in pars) else   None
    certno = pars['certno'][0]  if('certno'in pars) else   None
    
    if(isNone(msgid)):
        sendTextMsgToUser(user, '訊息已過期', caller.AccessToken)
        return False
    msg = load_from_db(msgid)
    
    
    if(isNone(msg) or is_overtime(msg['req_datetime'])):
        sendTextMsgToUser(user, '訊息已過期', caller.AccessToken)
        return False
    
    cert = get_DiagCertificate(docno, certno)
    if(not isNone(cert) and not isNone(cert[0]['DELETE_URL']) and cert[0]['DOC_NO'] == emp['EMP_NO']):
        request_api(cert[0]['DELETE_URL'])
 
        sendTextMsgToUser(user, '{0}-診斷書已刪除'.format(msg['rawdata']['PAT_NAME']), caller.AccessToken)
    elif(not isNone(cert) and cert[0]['DOC_NO'] != emp['EMP_NO']):
        sendTextMsgToUser(user, '人員身份認證錯誤無法刪除', caller.AccessToken)        
    else:
        sendTextMsgToUser(user, '{0}-診斷書已刪除'.format(msg['rawdata']['PAT_NAME']), caller.AccessToken)
        
        
        

def toImage(html):
    try:
        URI = "{0}/selenium-sv/api/discret/html2img".format(Config.K8S2_URL)
        req_data = {
            "html": html
        }
        headers={ 'Content-Type': 'application/json'}
        content = call_api_default(uri= URI, payload= json.dumps(req_data), headers= headers, timeout=30)
        return content

    except Exception as e:
        logger.error('toImage: {0}'.format(str(e))) 
        return None


def preview_discert(caller, data):
    now = datetime.now()
    ts = now.timestamp()
    user = data['events'][0]['source']['userId']
    emp =  data['empInfo']
    qs = data['events'][0]['data']
    pars = parse_qs(qs)
    msgid = pars['msgid'][0]  if('msgid'in pars) else   None
    docno = pars['docno'][0]  if('docno'in pars) else   None
    certno = pars['certno'][0]  if('certno'in pars) else   None
    
    if(isNone(msgid)):
        sendTextMsgToUser(user, '訊息已過期', caller.AccessToken)
        return False
    
    msg = load_from_db(msgid)
    
    if(isNone(msg) or is_overtime(msg['req_datetime'])):
        sendTextMsgToUser(user, '訊息已過期', caller.AccessToken)
        return False    
    
    cert = get_DiagCertificate(docno, certno)
    if(not isNone(cert) and not isNone(cert[0]['HTML'])):
        screenshot_as_bytes =  toImage(cert[0]['HTML'])
        imageid = upload_image(screenshot_as_bytes, caller.AccessToken)
        # -將image傳送給user
        msg = makeFlexMsg_DecertPreview(cert[0]['PAT_NAME'] ,imageid)
        sendFlexMsgToUser(user, msg, caller.AccessToken)
        
    else:
        sendTextMsgToUser(user, '已簽署或作廢無法瀏覽', caller.AccessToken)