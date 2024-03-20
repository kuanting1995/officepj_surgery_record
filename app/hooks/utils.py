
import json
from lib.cacheUtils import cache
from settings import Config
from lib.utils import call_api,call_api_get
from lib.logger import logger
from lib.Checker import isNone

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



# 用chartno獲取所有active order
def get_activeorder_all(chartno):
    rs = None
    try:
        URI = "{0}/slight/api/nis/inp/ActiveOrds".format(Config.K8S_URL)
        req_data = {
            # "ChartNo": '0682118',
            "ChartNo": chartno,
            "InpNo":"",
            "OrddRid":""
        }
        headers={ 'Content-Type': 'application/json'}
        content = call_api(uri= URI, payload= json.dumps(req_data), headers= headers)
        if(not isNone(content) ):
            rs = json.loads(content)
            # majorclass分類對應
            majorclass_mapping = {
            '0': '口服',
            '00': '針劑',
            '01': '外用',
            '02': '護理',
            '03': '病檢',
            '04': '其他'
            }

        # 為每個order添加 key-value,['MajorclassText']:'口服'
        for order in rs['data']:
            majorclass = order['MajorClass']
            order['MajorclassText'] = majorclass_mapping.get(majorclass, '')
    except Exception as e: 
        logger.error('get_activeorder_all: {0}'.format(str(e))) 
        return None
    return rs

# 用majorclass獲得分類active order
def get_activeorder_byClass(majorclass,ddl):
    rs = ddl
    if rs and 'data' in rs and majorclass is not None:
        rs['data'] = [item for item in rs['data'] if item['MajorClass'] == majorclass]
    return rs
# rs =  {
#      'status': True,
#      'message': '',
#      'data': [{
#          'NowStationNo': '05B',
#          'NowBedNo': '5251',
#          'InpNo': '00386619',
#          'ChartNo': '06758676',
#          'ChartSeq': 0,
#          'SeqNo': '2',
#          'CodeSeq': 11,
#          'CodeNo': '600720',
#          'MajorClass': '02',
#          'OrddTxt': 'GRAM STAIN＋AEROBIC CULTURE (組套) \r\n: Specimen: Sputum/Bacteria\r\n: Gram stain, Aerobic Culture\r\n: if get sputum out',
#          'CreDate': '20230911',
#          'CreTime': '1456',
#          'CreId': '003074',
#          'CreUserName': '丁熙安',
#          'EndTime': None,
#          'TotQty': 1.0,
#          'BeginDateTimeStr': '2023-09-11 14:48',
#          'MajorclassText': '護理'
#      }],
#  }

