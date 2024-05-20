import json
from lib.cacheUtils import cache
from settings import Config
from lib.logger import logger
from lib.Checker import isNone
from lib.utils import call_api,call_api_get
import requests
import base64


@cache.memoize(60)  
def get_in_patient_doc_list(user_id):
    rs = None
    try:
        URI = "{0}/slight/api/emp/InPatientDocList".format(Config.K8S2_URL)
        # 資料
        req_data = {
            "USER_ID": user_id
        }
        headers={ 'Content-Type': 'application/json'}
        content = call_api(uri= URI, payload= json.dumps(req_data), headers= headers, timeout=15)
        if(not isNone(content) ):
            rs = json.loads(content)
    except Exception as e: 
        logger.error('get_in_patient_doc_list: {0}'.format(str(e))) 
        return None
    return rs



@cache.memoize(60)  
def get_in_patient_by_doc(docno):
    rs = None
    try:
        URI = "{0}/slight/api/teamplus/GetInPatientListByDoc".format(Config.K8S2_URL)
        # 資料
        req_data = {
            "USER_ID": docno
        }
        headers={ 'Content-Type': 'application/json'}
        content = call_api(uri= URI, payload= json.dumps(req_data), headers= headers, timeout=15)
        if(not isNone(content) ):
            rs = json.loads(content)
            if(not isNone(rs['data'])):
                rs['data'] = sorted(rs['data'], key=lambda pat: pat['SEQNO'])
            
    except Exception as e: 
        logger.error('get_in_patient_doc_list: {0}'.format(str(e))) 
        return None
    return rs