import requests, os
import json
from  settings import Config
import base64

# CHANNEL_ACCESS_TOKEN = Config.TEST_IPB_CHANNEL_ACCESS_TOKEN

PRODUCTION = os.getenv('PRODUCTION', "False").strip()

if PRODUCTION in [True, 'true', 'True', 'TRUE']:
    CHANNEL_ACCESS_TOKEN = Config.IPB_CHANNEL_ACCESS_TOKEN
else:
    CHANNEL_ACCESS_TOKEN = Config.TEST_IPB_CHANNEL_ACCESS_TOKEN

# 傳Flex Messages給user
def sendFlexMsgToUser(user,msg):
    url = "https://team.kfsyscc.org/API/MessageFeedService.ashx"
    flexMsg = {
        "ask": "broadcastMessageByLoginNameList",
        "recipientList": [user],
        "message": msg
    }
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': CHANNEL_ACCESS_TOKEN 
        }
    x = requests.post(url, headers=headers, json=flexMsg)
    x.raise_for_status()
    return x.json()

def send_message(recipient, message):
    url = "https://eim.kfsyscc.org/API/MessageFeedService.ashx"

    # 簡易版通知（team+ 需開啟一對一交談）
    payload = {
        "ask": "sendMessage",
        "recipient": recipient,
        "message": {"type": "text", "text": message},
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": CHANNEL_ACCESS_TOKEN,
    }

    x = requests.post(url, headers=headers, json=payload)
    return x.json()

def updateFlexFooter(messagesn, user, finalMsg):
    url = "https://team.kfsyscc.org/API/MessageFeedService.ashx"
    data = {
        "ask": "updateFlexMessageFooter",
        "messageSN": messagesn,
        "recipient": user,
        "flexFooter": {
            "type": "text",
            "text": finalMsg,
            "fontColor": "#000000",
            "align": "center",
            "fontSize": 18
        }
    }
    headers = {
        'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cGUiOiJKV1QifQ.eyJ0eXBlIjowLCJleHAiOjAsImlkIjoyN30.2nws6R8Ddoy-7wYTckvfXlug-GKijPPmpnibGwtw6Y4',
        'Content-Type': 'application/json; charset=utf-8',
    }

    x = requests.post(url, headers=headers, json=data)
    print(f"Response content: {x.text}")
    if x.status_code != 200:
        print(f"Request failed with status code {x.status_code}")
        return None
    try:
        return x.json()
    except json.JSONDecodeError:
        print(f"Failed to parse JSON: {x.text}")
        return None
    

# 上傳image至 team+ server, 收到回傳token
def upload_image(image_data):
    url = "https://team.kfsyscc.org/API/MessageFeedService.ashx"
    
    #image_data是二進位json不支援, 無法傳送,轉成base64可用
    image_data_base64 = base64.b64encode(image_data).decode()
    # 簡易版通知（team+ 需開啟一對一交談）
    payload = {
        "ask": "uploadFile",
        "file_type":"png",
        "data_binary": image_data_base64
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": CHANNEL_ACCESS_TOKEN,
    }

    x = requests.post(url, headers=headers, json=payload)
    return x.json()

