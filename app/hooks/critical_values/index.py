from ..route import api_route, route_info

@api_route(rule='', params=None, methods=['GET'])
def index():
    '''{ "Description": "critical_values hook ", "Methods":"GET", "Content-Type":"application/json",
         "Parameters":[]
    }'''
    return route_info('critical_values')