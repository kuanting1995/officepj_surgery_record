
import json
from lib.cacheUtils import cache
from settings import Config
from lib.logger import logger
from lib.Checker import isNone
from lib.utils import call_api,call_api_get
import requests

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

# note:timeout=10->呼叫一個API或者執行一個可能需要等待的操作時，有時你可能不想讓程式無限期的等待。在這種情況下，你可以設置一個超時時間。


# 獲取病人基本資料
def get_med_info(pat_id):
    rs = None
    try:
        URI = "{0}/slight/api/nis/inp/GetInpInfo".format(Config.K8S_URL)
        # 資料"PID":"5902","USER_ID":"004909",
        req_data = {
            "PID": pat_id,
            "USER_ID": "004909"
        }
        headers={ 'Content-Type': 'application/json'}
        content = call_api(uri= URI, payload= json.dumps(req_data), headers= headers)
        if(not isNone(content) ):
            rs = json.loads(content)
    except Exception as e: 
        logger.error('get_user_info: {0}'.format(str(e))) 
        return None
    return rs
# rs = {
# "status": true,
# "message": "success",
# "data": {
# "CHART_NO": "06767248",
# "PAT_IDNO": "F104179477",
# "PAT_NAME": "夏O中",
# "SEX": "M",
# "BIRTHDAY": "19421025",
# "TEL_MOBILE": "0986608930",
# "EMAIL": "anyu726@gmail.com",
# "COM_CHART": null,
# "AGE": 81,
# "TEL_HOME": "02-27608930",
# "AREA_CODE": "105",
# "ADDRESS": "龍田里健康路135號3樓",
# "IDC_FLAGS": null,
# "PAT_IDNO_MASK": "F1******77",
# "PAT_NAME_MASK": "夏O中",
# "INP_NO": "00386423",
# "NOW_STATIONNO": "05C",
# "NOW_BEDNO": "5902",
# "IN_DATE": "20230912",
# "OUT_DATE": null,
# "DOC_NO1": "001355",
# "DOC_NAME1": "陳建志",
# "DOC_NO2": "001365",
# "DOC_NAME2": "謝英潔"
# }
# }



# 用chartno獲取所有active order(nis分類使用版)
def get_activeorder(chartno,inpno,ordertype):
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



# 獲取某病人所有active order的majorname list(top分類使用)
def get_majorname_list(inpno):
    # 发送 GET 请求
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

        # 如果你需要一个列表，可以将集合转换为列表
        majorname_list = list(majorname_set)

        return majorname_list
    else:
        print(f"请求失败，状态码：{response.status_code}")
        return None
    


# 輸入majorname(ordertype中文)可獲得active order(同top分類,slight api)
def get_activeorder_by_type(inpno,ordertype):
    rs = None
    try:
        # URI = "http://localhost:5000/slight/api/nis/inp/GetOrdbyType" +>測試用
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
        logger.error('get_activeorder_by_type: {0}'.format(str(e))) 
        return None
    return rs