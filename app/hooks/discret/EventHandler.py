
from flask import Flask, request, jsonify
import requests
from ..route import api_route 
from  settings import Config
from lib.Checker import isNationalIdentificationNumberValid, is8Num, is4Num, isNone
from hooks.utils import sendFlexMsgToUser, sendTextMsgToUser, upload_image
from lib.utils import call_api_get
from selenium import webdriver
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
from io import BytesIO
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


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
        sendTextMsgToUser(user, '診斷書已確認', caller.AccessToken)
    elif(not isNone(cert) and cert[0]['DOC_NO'] != emp['EMP_NO']):
        sendTextMsgToUser(user, '人員身份認證錯誤無法簽章', caller.AccessToken)
    else:
        sendTextMsgToUser(user, '診斷書已確認', caller.AccessToken)

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
 
        sendTextMsgToUser(user, '診斷書已刪除', caller.AccessToken)
    elif(not isNone(cert) and cert[0]['DOC_NO'] != emp['EMP_NO']):
        sendTextMsgToUser(user, '人員身份認證錯誤無法刪除', caller.AccessToken)        
    else:
        sendTextMsgToUser(user, '診斷書已刪除', caller.AccessToken)
        
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
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")  # 選擇無頭模式運行
        options.headless = True
         
        
        options.add_argument("--headless")  # 啟用無頭模式
        options.add_argument("--disable-gpu")  # 禁用 GPU 硬件加速
        options.add_argument("--no-sandbox")  # 禁用沙盒（在 Docker 和某些 Linux 環境下運行時需要）
        options.add_argument("--disable-dev-shm-usage")  # 禁用 /dev/shm 使用
        options.add_argument("--remote-debugging-port=9222")  # 設置遠程調試端口

        if(Config.APP_MODE == 'DEV'):
            service = Service(ChromeDriverManager().install())  
        else:
            # 如果是在 Docker 容器中運行，確保指定 binary 路徑
            options.binary_location = "/usr/bin/google-chrome"
            service = Service(executable_path="/usr/local/bin/chromedriver")  # 替換為實際的 ChromeDriver 路徑
              

        
        driver = webdriver.Chrome(service=service, options=options)  
        driver.set_window_size(794, 1122)
        driver.get("data:text/html;charset=UTF-8,{html_content}".format(html_content=cert[0]['HTML']))
        driver.execute_script("document.body.style.fontFamily = 'WenQuanYi Zen Hei';")
         
        # Set the size of the window to capture full page
        # 獲取截圖為 PNG 格式的字節數據
        screenshot_as_bytes = driver.get_screenshot_as_png()  # 返回截圖的字節數據
        driver.quit()
        imageid = upload_image(screenshot_as_bytes, caller.AccessToken)
        # -將image傳送給user
        msg = makeFlexMsg_DecertPreview(cert[0]['PAT_NAME'] ,imageid)
        sendFlexMsgToUser(user, msg, caller.AccessToken)
        
    else:
        sendTextMsgToUser(user, '診斷書無法瀏覽', caller.AccessToken)