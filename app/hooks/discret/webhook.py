
from flask import Flask, request, jsonify
import requests
from ..route import api_route 
from  settings import Config
from lib.Checker import isNone
import uuid
from urllib.parse import parse_qs
from datetime import datetime

from lib.logger import logger
from .EventHandler import BotEventHandler
from hooks.utils import get_med_info,get_vitalsignData,get_activeorder_all, get_user_info_by_ad
from hooks.utils import sendTextMsgToUser
from .utils import save_to_db, CHANNEL_ACCESS_TOKEN



@api_route(rule = '', params=None ,methods=['POST', 'GET'])
def _webhook():
    if not request.data:
        return "Webhook received!"

    bot = BotEventHandler(CHANNEL_ACCESS_TOKEN)
    
    data = request.json
    data['empInfo'] = None
    uid = data['events'][0]['source']['userId']
    
    emp = get_user_info_by_ad(uid)
    if(isNone(emp) or (not emp['status']) or isNone(emp['data']) ):
        msg= "未授權的使用者"
        sendTextMsgToUser(uid, msg, CHANNEL_ACCESS_TOKEN) 
        logger.error(msg)
        return msg
    else:
        data['empInfo'] = emp['data']

        
        
    bot.handle_event(data['events'][0]['type'], data)
    return data    

