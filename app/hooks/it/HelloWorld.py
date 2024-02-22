
from lib.utils import api_response
from ..route import api_route
from datetime import datetime   
from lib.cacheUtils import cache


req_params = {}
req_params['NAME'] = ['required']

@api_route(rule = '', params=req_params ,methods=['POST', 'GET'])
def _HelloWorld(args):
    '''{ "Description": "HelloWorld", "Methods":"POST", "Content-Type":"application/json",
         "Parameters":[
             {"Description":"NAME", "Name":"NAME", "Required":true}

         ]
    }'''    
    
    response_data = {}

    def _check_parameter():
        args['now'] = datetime.now()
        cachetest()
 
    def _deal():
        pass
    
    def _responseData():
        response_data['status'] = True
        response_data['message'] =  ''
        response_data['data'] = "Hello {0}".format(args['NAME']) 

        return response_data
    try:
        _check_parameter()
        _deal() 
        return api_response(_responseData()), 200
    except Exception as e:
        rs = {'status':False, 'message': str(e), 'data': None}  
        return api_response(rs), 400
    finally:
        pass
            
 
@cache.memoize(600)   
def cachetest():
    return "test"    
