from flask import Blueprint
from settings import Config
from lib.utils import  api_response, logger
from lib.web import get_parameter
from lib.Checker import isNone
import re 
import pkgutil 
from flask import  render_template
from flask import current_app as app
import json
import os

# 获取目录的名称（不包括其路径）
directory_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
prefix = directory_name
apiprint = Blueprint(prefix, __name__)
@apiprint.route('/', methods=['GET'])
def index():
    """API列表 (＊Token required )"""
    return route_info(prefix)

urlcheck = re.compile(r'^{0}(\.\w+)+'.format(prefix)) 

def api_route(bpt=apiprint, rule=None, params=None, **options):
    def decorator(func):
        encode_rule = rule
        if (rule is not None and rule == '/'):
            '''routing by function name'''
            encode_rule = '/{0}'.format(func.__name__)
        elif (rule is None or len(str(rule)) == 0):
            '''routing by file name'''
            encode_rule = ''
        
        path = ''
        
        if(urlcheck.match(func.__module__) is None):
            logger.error('API Blueprint: invalid api path!')
            if(Config.DEBUG):
                raise Exception('API Blueprint: invalid api path!')   
        else:
            path = '/{0}{1}'.format('/'.join(re.split(r'\b\.\b', func.__module__)[1:]), encode_rule)

        options.update( {'endpoint' : path} )
        
        @bpt.route(path, **options)
        def route_wrapper(*args, **kwargs):
            try:
                if(not isNone(params)):
                    kwargs['args'] = get_parameter(**params)
                return func(*args, **kwargs)                         
            except ValueError as e:
                rs = {'success':False, 'message': str(e), 'data': []}  
                return api_response(rs), 400
        route_wrapper.__doc__ = func.__doc__    
        return route_wrapper
    return decorator



urlcheck_root = re.compile(r'^{0}\.'.format(prefix)) 

def route_info(prefix):
    """Print available functions."""
    func_list = []
    for rule in app.url_map.iter_rules():
        #if rule.endpoint != 'static' and rule.endpoint !=  'surl.index':
        if(urlcheck_root.match(rule.endpoint) is not None):
            if (prefix == None) or ("/{}/".format(prefix) in rule.rule):
                finc = {}
                #pathname = "" if request.path == "/" else request.path
                finc['uri'] = '{0}'.format(rule.rule)
                finc['endpoint'] = '{0}'.format(rule.endpoint)
                finc['method'] = 'POST' if('POST' in rule.methods) else 'GET'
                finc['methodPost'] = 'POST' if('POST' in rule.methods) else None
                finc['methodGet'] = 'GET' if('GET' in rule.methods) else None
                try:
                    doct = json.loads(
                        s=app.view_functions[rule.endpoint].__doc__)
                    finc['doc'] = doct
                except Exception as e:
                    finc['doc'] = app.view_functions[rule.endpoint].__doc__

                func_list.append(finc)
    return render_template('index.html', docs=func_list, app_root=app.config['APPLICATION_ROOT'])