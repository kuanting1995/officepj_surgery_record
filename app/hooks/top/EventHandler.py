
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
import inspect


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

def comfirm_discert(caller, data):
    user = data['events'][0]['source']['userId']
    emp =  data['empInfo']
    qs = data['events'][0]['data']
    pars = parse_qs(qs)
    docno = pars['docno'][0]  if('docno'in pars) else   None
    certno = pars['certno'][0]  if('certno'in pars) else   None
    
    cert = get_DiagCertificate(docno, certno)
    if(not isNone(cert) and not isNone(cert[0]['CONFIRM_URL']) and cert[0]['DOC_NO'] == emp['EMP_NO']):
        print(emp['EMP_NO'])
    #    res = call_api_get(cert[0]['CONFIRM_URL'])
        sendTextMsgToUser(user, '診斷書已確認', caller.AccessToken)
    elif(cert[0]['DOC_NO'] != emp['EMP_NO']):
        sendTextMsgToUser(user, '人員身份認證錯誤無法簽章', caller.AccessToken)
        
    else:
        sendTextMsgToUser(user, '診斷書已確認', caller.AccessToken)

def delete_discert(caller, data):
    user = data['events'][0]['source']['userId']
    emp =  data['empInfo']
    qs = data['events'][0]['data']
    pars = parse_qs(qs)
    docno = pars['docno'][0]  if('docno'in pars) else   None
    certno = pars['certno'][0]  if('certno'in pars) else   None
    
    cert = get_DiagCertificate(docno, certno)
    if(not isNone(cert) and not isNone(cert[0]['DELETE_URL']) and cert[0]['DOC_NO'] == emp['EMP_NO']):
        sendTextMsgToUser(user, '診斷書已刪除', caller.AccessToken)
    elif(cert[0]['DOC_NO'] != emp['EMP_NO']):
        sendTextMsgToUser(user, '人員身份認證錯誤無法刪除', caller.AccessToken)        
    else:
        sendTextMsgToUser(user, '診斷書已刪除', caller.AccessToken)
        
def preview_discert(caller, data):
    user = data['events'][0]['source']['userId']
    emp =  data['empInfo']
    qs = data['events'][0]['data']
    pars = parse_qs(qs)
    docno = pars['docno'][0]  if('docno'in pars) else   None
    certno = pars['certno'][0]  if('certno'in pars) else   None
    
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

        if(Config.APP_MODE == 'TEST'):
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