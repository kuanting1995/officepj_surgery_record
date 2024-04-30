from hooks.route import api_route, route_info

@api_route(rule='', params=None, methods=['GET'])
def index():
    '''{ "Description": "診斷書簽署服務頻道 APIs", "Methods":"GET", "Content-Type":"application/json",
         "Parameters":[]
    }'''
    return route_info('discret')