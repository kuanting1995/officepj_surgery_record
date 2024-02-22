from flask import current_app
import math
import socket
from sqlalchemy.orm.state import InstanceState
from uuid import UUID
from flask import jsonify, request, Response, render_template
from flask import current_app as app
from flask_caching import Cache
from functools import wraps
import dicttoxml
from decimal import Decimal
import json
from datetime import datetime, timedelta, date
from settings import Config, Message
import time
import re
import base64
from lib.logger import logger



def before_request(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        print(1, request.headers.get('User-Agent'))
        return f(*args, **kwargs)
    return decorated


time_offset = int((time.altzone/3600))
time_offset_str = str(
    time_offset) if time_offset > 0 else '+{0}'.format(str(-time_offset))


def jsonconverter(o):
    if isinstance(o, datetime):
        return o.strftime("%a %b %d %Y %H:%M:%S GMT{0}".format(time_offset_str))
    elif isinstance(o, InstanceState):
        return o.__str__()
    elif isinstance(o, UUID):
        return o.__str__()
    # elif isinstance(o, cx_Oracle.LOB):
    #     return o.read()
    elif isinstance(o, Decimal):
        return float(o)
    else:
        return o.__str__()

# api response format

def api_response(data):
    if ((not data) and (type(data) == list )) :
        return jsonify([])
    elif ((not data) and (type(data) == dict )) :
        return jsonify({})
    elif not data:
        return jsonify(None)

    content_type = request.headers.get('Content-Type')

    if (content_type == 'application/xml') or (content_type == 'text/xml'):
        return Response(dicttoxml.dicttoxml(data), mimetype='application/xml')
    else:
        return Response(json.dumps(data, default=jsonconverter, ensure_ascii=False), mimetype='application/json', headers={'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Credentials': 'true'})

def json_response(jsonstr):

    if not jsonstr:
        return jsonify({'status': 400, 'message': 'Posted data not matched!'})

    return Response(jsonstr, mimetype='application/json')


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('172.16.254.51', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


# 獲取本月第一天
def first_day_of_month():
    return date.today() - timedelta(days=datetime.now().day - 1)

# 獲取本週第一天


def first_day_of_week():
    return date.today() - timedelta(days=date.today().weekday())

# 獲取本週最後一天


def last_day_of_week():
    return date.today() + timedelta(days=(6-date.today().weekday()))


_default_hex_code = '0123456789abcdefghigklmnopqrstuvwxyzABCDEFGHIGKLMNOPQRSTUVWXYZ'

# 10進制轉Hex


def string_10toHex(number, hex_code=_default_hex_code):
    charsArr = list(hex_code)
    radix = len(charsArr)
    qutient = +number
    arr = []
    while(qutient):
        mod = int(qutient % radix)
        qutient = (qutient - mod) / radix
        arr.insert(0, charsArr[mod])
    return "".join(arr)


# Hex10轉進制


def string_HexTo10(number, hex_code=_default_hex_code):
    radix = len(hex_code)
    number_code = list(str(number))
    nolen = len(number_code)
    i = 0
    origin_number = 0
    while(i < nolen):
        a = math.pow(radix,  i)
        i = i+1
        b = hex_code.index(number_code[nolen - i])
        origin_number += b * a
    return int(origin_number)

import requests
import ssl
from urllib3 import poolmanager


class TLSAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        """Create and initialize the urllib3 PoolManager."""
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        self.poolmanager = poolmanager.PoolManager(
                num_pools=connections,
                maxsize=maxsize,
                block=block,
                #ssl_version=ssl.PROTOCOL_TLSv1,
                ssl_version=ssl.PROTOCOL_TLSv1_2,
                ssl_context=ctx
                )

def call_api(uri, payload, headers={ 'Content-Type': 'application/json' }, timeout=12, retries=3, datafiles = None):
    try:
        requests.adapters.DEFAULT_RETRIES = retries #重連次數 
        s = requests.session()
        try:
            isHttps = uri.index('https://')
            if(isHttps == 0):
                s.mount('https://', TLSAdapter())
        except Exception as e:
            pass
            #logger.info('call_api_mount:{0}'.format(str(e)))
        
        s.keep_alive = False # 關閉多餘連結
        r = s.post(uri, headers=headers, data=payload, timeout= timeout, files = datafiles).content
        pythonObj = r.decode('utf-8')
        return pythonObj
    except Exception as e: 
        logger.error('call_api:{0}'.format(str(e)))
        return None
    finally:
        # 關閉請求 釋放內存
        s.close()
        del(s)
       

def call_api_get(uri, headers={ 'Content-Type': 'application/json' }, timeout=12, retries=3):
    try:
        requests.adapters.DEFAULT_RETRIES = retries #重連次數 
        s = requests.session()
        try:
            isHttps = uri.index('https://')
            if(isHttps == 0):
                s.mount('https://', TLSAdapter())
        except Exception as e:
            logger.info('call_api_get_mount:{0}'.format(str(e)))

        
        s.keep_alive = False # 關閉多餘連結
        r = s.get(uri, headers=headers, timeout= timeout).content
        pythonObj = r.decode('utf-8')
        return pythonObj
    except Exception as e: 
        logger.error('call_api_get:{0}'.format(str(e)))
        return None
    finally:
        # 關閉請求 釋放內存
        s.close()
        del(s)

def lineMsg(msg, chartno=None, empno=None):
    urlStr = "https://www.kfsyscc.org/kfccbot/api/bothook/pushTextMessage"
    headers={ 'Content-Type': 'application/json'}
    payload={}
    payload['apiKey'] = 'Kfsyscc2160@MisTest'
    payload['ChartNO'] = chartno
    payload['EmpNO'] = empno
    payload['Message'] = msg
    postBody =json.dumps(payload)
    rawdata = call_api(uri= urlStr, payload= postBody, headers= headers, timeout=10)


def camel_case(s):
  s = re.sub(r"(_|-)+", " ", s).title().replace(" ", "")
  return ''.join([s[0].lower(), s[1:]])

def base64_encode(str_data):
    """
    Base64Url
    加base64
    :type bytes_data: byte
    :rtype return: string
    """
    bytes_data = str_data.encode('UTF-8')
    output = base64.b64encode(bytes_data).decode('utf8')
    output = output.split('=')[0]
    output = output.replace('+', '-')
    output = output.replace('/', '_')
    
    return output


def base64_decode(str_data):
    """
    Base64Url
    解base64
    :type str_data: string
    :rtpe return: byte
    """
    output = str_data
    output = output.replace('-', '+')
    output = output.replace('_', '/')

    pad = len(output) % 4

    if(pad == 0):
        pass
    elif(pad == 2):
        output += "=="
    elif(pad == 3):
        output += "="
    else:
        raise Exception("Illegal base64url string!")   

    return base64.b64decode(output.encode('utf-8')).decode("utf-8")




MIMI_TYPES={
'pdf':'application/pdf',
'jpeg':'image/jpeg',
'png':'image/png',
'jpg':'image/jpg',
'gif':'image/gif',
'txt':'text/plain',
'doc':'application/msword',
'docx':'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
}



def idmask(code):
    if len(code) >= 4 :
        code = code[0:2] +'******'+ code[len(code)-2:len(code)] 
        return code
    else:
        return '****'

def phonemask(code):
    if len(code) >= 5 :
        code = code[0:3] +'****'+ code[len(code)-2:len(code)] 
        return code
    else:
        return '****' 

def namemask(code):
    mask = "O"
    if len(code) == 1:
        return code
    if len(code) <= 2 :
        code = code[0] +mask 
        return code
    if len(code) > 2 :
        code = code[0] +(mask*(len(code)-2))+ code[len(code)-1:len(code)] 
        return code    
    else:
        return code