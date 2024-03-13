# -*- coding: utf-8 -*-
from functools import wraps
from flask import  request, jsonify
import base64
from lib.Checker import isNone
import urllib.parse
from settings import Config, Message
from .cacheUtils import cache
from lib.AESCipher import AESCipher

def get_parameter(**_params):
    return  _get_parameter(**_params)

def _get_parameter(**_params):
    _result = {}

    if request.method in ['POST', 'DELETE'] :

        content = request.get_json() if request.is_json else (request.form if request.form else [])
        for key, value in _params.items():
            if (key in content):
                _result[key] =  content[key]
            elif (key.lower() in content):
                _result[key] =  content[key.lower()]
            else:
                _result[key] = None

            if ('required' in value):
                if (key not in _result) or isNone(_result[key]):
                    raise ValueError('{0} is required.'.format(key))

            if('base64' in value):
                if (not isNone(_result[key])):
                    _result[key] = str(base64.b64decode(_result[key]).decode("utf-8") ) 
            
            if('uriDecode' in value):
                if (not isNone(_result[key])):
                    _result[key] = urllib.parse.unquote_plus(_result[key])
            
    elif request.method == 'GET':
        for key, value in _params.items():
            if (request.args.get(key) is not None):
                _result[key] =  request.args.get(key) 
            elif (request.args.get(key.lower()) is not None):
                _result[key] =  request.args.get(key.lower()) 
            else:
                _result[key] = None

            if ('required' in value):
                if isNone(_result[key]):
                    raise ValueError('{0} is required.'.format(key))
                    
            if('base64' in value):
                if (not isNone(_result[key])):
                    _result[key] = str(base64.b64decode(_result[key]).decode("utf-8"))

            if('uriDecode' in value):
                if (not isNone(_result[key])):
                    _result[key] = urllib.parse.unquote_plus(_result[key])

    return _result


METHODS={
    "QUERYSTRING":"QUERYSTRING",
    "HEADER":"HEADER",
    "COOKIE":"COOKIE"
}

API_KEY_NAME = 'x-api-key'
API_AUTH_NAME = 'Authorization'
@cache.memoize(300)
def validateAuthorization(token, method, apifor=['*']):
    encrypt= AESCipher(Config.SYS_AES_KEY).decrypt(token)
    if('*' not in apifor and encrypt not in apifor):
        return False
    if(METHODS['QUERYSTRING'] == method and encrypt != "KFSYSCC"):
        return False
    return True

# 自定義的帶參數的裝飾器
def apikey_required(apifor=['*']):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                method = None
                token = None
                if API_KEY_NAME in request.headers:
                    method =METHODS['HEADER']
                    token = request.headers[API_KEY_NAME]
                    
                    
                if not token:
                    method =METHODS['COOKIE']
                    token = request.cookies.get(API_KEY_NAME)
                    
                if not token:
                    method =METHODS['QUERYSTRING']
                    if request.method in ['POST', 'DELETE'] :                             
                        content = request.get_json() if request.is_json else (request.form if request.form else [])  
                        token =  content[API_KEY_NAME] 
                    elif request.method == 'GET':
                        token =  request.args.get(API_KEY_NAME) 
                        
                if not token:
                    return jsonify({'status': False, 'message': Message.APIKEY_IS_MISING}), 401

                if(not validateAuthorization(token, method, apifor)):
                    return jsonify({'status': False, 'message': Message.APIKEY_IS_UNAUTH}), 401 
                    
            except Exception as e:
                return jsonify({'status': False, 'message': Message.APIKEY_IS_UNAUTH}), 401
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

