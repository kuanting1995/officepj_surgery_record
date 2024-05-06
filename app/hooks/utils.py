import json
from lib.cacheUtils import cache
from settings import Config
from lib.logger import logger
from lib.Checker import isNone
from lib.utils import call_api,call_api_get
import requests
import base64


# 傳Flex Messages給user
def sendFlexMsgToUser(user,msg, accessToken):
    url = "{0}/API/MessageFeedService.ashx".format(Config.TEAM_SERVER)
    
    flexMsg = {
        "ask": "broadcastMessageByLoginNameList",
        "recipientList": [user],
        "message": msg
    }
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': accessToken 
        }
    x = requests.post(url, headers=headers, json=flexMsg, timeout=10)
    x.raise_for_status()
    return x.json()

@cache.memoize(10)  
def sendTextMsgToUser(recipient, message, accessToken):
    url = '{0}/API/MessageFeedService.ashx'.format(Config.TEAM_SERVER)
    # 簡易版通知（team+ 需開啟一對一交談）
    payload = {
        "ask": "sendMessage",
        "recipient": recipient,
        "message": {"type": "text", "text": message},
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": accessToken,
    }

    x = requests.post(url, headers=headers, json=payload, timeout=10)
    x.raise_for_status()
    return x.json()

def updateFlexFooter(msgID, username, finalMsg, accessToken):
    url = "{0}/API/MessageFeedService.ashx".format(Config.TEAM_SERVER)
    data = {
        "ask": "updateFlexMessageFooter",
        "messageSN": msgID,
        "recipient": username,
        "flexFooter": {
            "type": "text",
            "text": finalMsg,
            "fontColor": "#000000",
            "align": "center",
            "fontSize": 14
        }
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": accessToken
    }

    x = requests.post(url, headers=headers, json=data)
    return x.json()

# 上傳image至 team+ server, 收到回傳token
@cache.memoize(86400)  
def upload_image(image_data, accessToken):
    url = "{0}/API/MessageFeedService.ashx".format(Config.TEAM_SERVER)
    
    #image_data是二進位json不支援, 無法傳送,改用base64
    image_data_base64 = base64.b64encode(image_data).decode()
    # 簡易版通知（team+ 需開啟一對一交談）
    payload = {
        "ask": "uploadFile",
        "file_type":"png",
        "data_binary": image_data_base64
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": accessToken,
    }
    x = requests.post(url, headers=headers, json=payload, timeout=15)
    return x.json()

@cache.memoize(3600)  
def get_user_info(user_id):
    rs = None
    try:
        URI = "{0}/slight/api/emp/CurrentEmployee".format(Config.K8S_URL)
        # 資料
        req_data = {
            "EMP_NO": user_id,
            "USER_ID": "KFSYSCC"
        }
        headers={ 'Content-Type': 'application/json'}
        content = call_api(uri= URI, payload= json.dumps(req_data), headers= headers, timeout=10)
        if(not isNone(content) ):
            rs = json.loads(content)
    except Exception as e: 
        logger.error('get_user_info: {0}'.format(str(e))) 
        return None
    return rs


@cache.memoize(14400)  
def get_user_info_by_email(email):
    rs = None
    try:
        URI = "{0}/slight/api/emp/CurrentEmployeeByEmail".format(Config.K8S_URL)
        # 資料
        req_data = {
            "EMAIL": email,
            "USER_ID": "KFSYSCC"
        }
        headers={ 'Content-Type': 'application/json'}
        content = call_api(uri= URI, payload= json.dumps(req_data), headers= headers, timeout=10)
        if(not isNone(content) ):
            rs = json.loads(content)
    except Exception as e: 
        logger.error('get_user_info: {0}'.format(str(e))) 
        return None
    return rs


def get_user_info_by_ad(ad):
    return get_user_info_by_email("{0}@kfsyscc.org".format(ad))
# note:timeout=10->呼叫一個API或者執行一個可能需要等待的操作時，有時你可能不想讓程式無限期的等待。在這種情況下，你可以設置一個超時時間。


# 獲取病人基本資料
@cache.memoize(600)
def get_med_info(pat_id, userid):
    rs = None
    try:
        URI = "{0}/slight/api/nis/inp/GetInpInfo".format(Config.K8S_URL)
        # 資料"PID":"5902","USER_ID":"004909",
        req_data = {
            "PID": pat_id,
            "USER_ID": userid
        }
        headers={ 'Content-Type': 'application/json'}
        content = call_api(uri= URI, payload= json.dumps(req_data), headers= headers)
        if(not isNone(content) ):
            rs = json.loads(content)
    except Exception as e: 
        logger.error('get_user_info: {0}'.format(str(e))) 
        return None
    return rs


# 獲取某病人所有active order的majorname list(top分類使用)
def get_majorname_list(inpno):
    URL = "{0}/topapi/note/doc_order_inp/".format(Config.K8S_URL)+inpno
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        # 创建一个空集合来存储 "MAJOR_NAME" 的值，并自动处理重复的值
        majorname_set = set()
        # 遍历数据
        for item in data:
            # 获取 "majorname_NAME" 的值
            major_name = item["MAJOR_NAME"]
            # 将 "MAJOR_NAME" 添加到集合中
            majorname_set.add(major_name)
        # 集合转换为列表
        majorname_list = list(majorname_set)
        
        return majorname_list
    else:
        print(f"请求失败，状态码：{response.status_code}")
        return None
    
    
# 輸入majorname(ordertype中文)可獲得active order(top分類)
def get_activeorder_by_type(inpno,ordertype):
    rs = None
    try:
        URI = "{0}/slight/api/nis/inp/GetOrdbyType".format(Config.K8S_URL)
        req_data = {
            "InpNo": inpno,
            "OrderType": ordertype
        }
        headers={ 'Content-Type': 'application/json'}
        content = call_api(uri= URI, payload= json.dumps(req_data), headers= headers)
        if(not isNone(content) ):
            rs = json.loads(content)
    except Exception as e:
        logger.error('get_activeorder_by_type: {0}'.format(str(e))) 
        return None
    return rs['data']

#最新執行 active (top分類)
def get_orderRecent(inpno):
    rs = None
    try:
        URI = "{0}/topapi/note/doc_order_inpexe_all/".format(Config.K8S_URL)+inpno
        headers = { 'Content-Type': 'application/json'}
        response = requests.get(URI, headers=headers)
        content = response.content
        if content:
            rs = json.loads(content)
    except Exception as e:
        logger.error('get_orderRecent: {0}'.format(str(e))) 
        return None
    return rs

# 用chartno獲取所有active order(NIS分類)
def get_activeorder_all(chartno,inpno,ordertype):
    rs = None
    try:
        URI = "{0}/slight/api/nis/inp/ActiveOrds".format(Config.K8S_URL)
        req_data = {
            # "ChartNo": '0682118',
            "ChartNo": chartno,
            "InpNo": inpno,
            "OrddRid":"",
            "OrderType": ordertype
        }
        headers={ 'Content-Type': 'application/json'}
        content = call_api(uri= URI, payload= json.dumps(req_data), headers= headers)
        if(not isNone(content) ):
            rs = json.loads(content)
    except Exception as e: 
        logger.error('get_user_info: {0}'.format(str(e))) 
        return None
    return rs

@cache.memoize(300)
def get_vitalsignData(chartno,searchdate,intervaldays):
    rs = None
    try:
        # URI = "http://127.0.0.1:5000/slight/api/teamplus/GetVitalInp"
        URI = "{0}/slight/api/teamplus/GetVitalInp".format(Config.K8S_URL)
        req_data = {
            "Chartno": chartno,
            "SearchDate": searchdate,
            "IntervalDays":intervaldays
        }
        headers={ 'Content-Type': 'application/json'}
        content = call_api(uri= URI, payload= json.dumps(req_data), headers= headers)
        if(not isNone(content) ):
            rs = json.loads(content)
    except Exception as e:
        logger.error('get_vitalSignData: {0}'.format(str(e))) 
        return None
    return rs['data']

# 獲得檢驗檢查summary
def get_Lab(top,chartno):
    rs = None
    try:
        # URI = "http://127.0.0.1:5000/slight/api/teamplus/GetLab"=>測試
        URI = "{0}/slight/api/teamplus/GetLab".format(Config.K8S_URL)
        req_data = {
            "Top":top,
            "Chartno": chartno
        }
        headers={ 'Content-Type': 'application/json'}
        content = call_api(uri= URI, payload= json.dumps(req_data), headers= headers)
        if(not isNone(content) ):
            rs = json.loads(content)
    except Exception as e:
        logger.error('get_Lab: {0}'.format(str(e))) 
        return None
    return rs['data']


# 1.由top api獲得檢驗檢查 details 2.篩選日期前5筆並處理成需要的格式

def get_LabDetails(chartno, category, date):
    rs = None
    try:
        URI = "{0}/topapi/exam/lab_period/{1}/{2}".format(Config.K8S_URL, chartno, category)
        req_data = {
            "Chartno": chartno,
            "Category": category
        }
        headers = {'Content-Type': 'application/json'}
        content = call_api(uri=URI, payload=json.dumps(req_data), headers=headers)
        if content:
            rs = json.loads(content)
            
            # 1.從rs['das']篩選含date的最新4筆日期
            latest_4_dates = []
            if date in rs['das']:
                latest_4_dates = sorted([d for d in rs['das'] if d <= date], reverse=True)[:4]
            else:
                latest_4_dates = sorted([d for d in rs['das'] if d < date], reverse=True)[:4]
                
            # 2.抓出所有name 並將latest_4_dates中有值的填入name下
            # 建立一個以 name 為 key 的字典，並初始化所有日期的值為空字符串
            rows_dict = {row['name']: {date: '-' for date in latest_4_dates} for row in rs['rows']}

            # 更新字典中的值
            for row in rs['rows']:
                for date in latest_4_dates:
                    if date in row:
                        rows_dict[row['name']][date] = row[date][0][1]

            # 轉換為需要的格式
            result_data = [{'name': name, **dates} for name, dates in rows_dict.items()]
            return {
                "latest_4_dates": latest_4_dates,
                "result_data": result_data
            }
    except Exception as e:
        logger.error('get_LabDetails: {0}'.format(str(e))) 
        return None
    
    
@cache.memoize(60)  
def emrlog(empno, cNo, pgid, memo):
    try:
        URI = "{0}/topapi/staff/emrlog".format(Config.K8S_URL)
        # 資料
        req_data = {
            "empno": empno,
            "chartno": cNo,
            "prog": pgid,
            "memo": memo
        }
        headers={ 'Content-Type': 'application/json'}
        return call_api(uri= URI, payload= json.dumps(req_data), headers= headers, timeout=5)

    except Exception as e: 
        logger.error('emrlog: {0}'.format(str(e))) 
        return None
