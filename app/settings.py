import os
from flask import has_request_context, request
import logging
import urllib

basedir = os.path.abspath(os.path.dirname(__file__))
tmpdir = os.getenv('TMPDIR', '/tmp')


class Config(object):
    G_WORKERS = int(os.getenv('GUNICORN_WORKERS', '2'))
    APPLICATION_NAME = os.getenv('APPLICATION_NAME', 'hookap')
    APPLICATION_ROOT = os.getenv('APPLICATION_ROOT', '/hookap')
    DEBUG = (os.getenv('FK_DEBUG', 'False') == 'True')
    APP_MODE = os.getenv('FK_APP_MODE', 'TEST')
    SYSLOG_URL = os.getenv('FK_SYSLOG_URL', 'syslog.kfsyscc.org')
    SYSLOG_PORT = int(os.getenv('FK_SYSLOG_PORT', '5509'))
    JSON_AS_ASCII = False
    SECRET_KEY = 'BwcKCQMEDwAEDgsCBAkICw'
    K8S_URL =  os.getenv('FK_K8S_URL', 'https://ing.kfsyscc.org')
    NAPI_URL =  os.getenv('FK_NAPI_URL', 'https://napi.kfsyscc.org')
    GATEWAY_URL =  os.getenv('FK_GATEWAY_URL', 'http://hisweb3.kfcc.intra')
    K8S2_URL =  os.getenv('FK_K8S2_URL', 'https://ing-test.kfsyscc.org')
    


#hooks token
    IT_CHANNEL_ACCESS_TOKEN = os.getenv('FK_IT_CHANNEL_ACCESS_TOKEN', 'eyJhbGciOiJIUzI1NiIsInR5cGUiOiJKV1QifQ.eyJ0eXBlIjowLCJleHAiOjAsImlkIjoyfQ.K2ZsjFzSHGQTeUHPaMAZ2h59nWNpSHbgPiEPv6pVNG0')

# SYSCC
    SYS_AES_KEY = os.getenv('FK_SYS_AES_KEY', 'KfSyScC')

# REDSIS
    REDIS_HOST = os.getenv('FK_REDIS_HOST', "172.16.253.29")
    REDIS_PORT = int(os.getenv('FK_REDIS_PORT', 6379))
    REDIS_PASSWORD = os.getenv('FK_REDIS_PASSWORD', "pwd123456")
    REDIS_SOCKET_TIMEOUT = os.getenv('FK_REDIS_SOCKET_TIMEOUT', 5)
    REDIS_CONNECTION_TIMEOUT = os.getenv('FK_REDIS_CONNECTION_TIMEOUT', 3)
    CACHE_REDIS_URL = os.getenv('FK_CACHE_REDIS_URL', "redis://:{0}@{1}:{2}/2".format(
    REDIS_PASSWORD, REDIS_HOST,  REDIS_PORT   
    ))

           
class Message(object):
    TOKEN_IS_MISING = 'Access token is missing in the authorization http request head.'


        
class ReverseProxied(object):
    def __init__(self, app, script_name=None, scheme=None, server=None):
        self.app = app
        self.script_name = script_name
        self.scheme = scheme
        self.server = server

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '') or self.script_name
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]
        scheme = environ.get('HTTP_X_SCHEME', '') or self.scheme
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        server = environ.get('HTTP_X_FORWARDED_SERVER', '') or self.server
        if server:
            environ['HTTP_HOST'] = server
        return self.app(environ, start_response)


def GetXClientIP(request):
    try:
        return request.headers["X-ClientIP"]
    except Exception as e:
        return request.remote_addr

class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = GetXClientIP(request)
            record.app_name = Config.APPLICATION_NAME
        else:
            record.url = None
            record.remote_addr = None
            record.app_name = Config.APPLICATION_NAME
        return super().format(record)