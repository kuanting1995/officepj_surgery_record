
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
 


