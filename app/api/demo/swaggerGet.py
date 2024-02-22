
from lib.utils import api_response
from ..route import api_route
from datetime import datetime   
from lib.cacheUtils import cache
from flasgger import Swagger, swag_from

req_params = {}
req_params['name'] = ['']
req_params['type'] = ['']


@api_route(rule = '', params=req_params ,methods=['GET'])
def _swaggerGet(args):
    """
    Get items from the server
    ---
    parameters:
      - name: name
        in: query
        type: string
        required: false
        description: The type of items to return
      - name: type
        in: query
        type: string
        required: false
        description: The maximum number of items to return
    responses:
      200:
        description: Item created successfully
        schema:
          type: object
          properties:
            message:
              type: string
            status:
              type: boolean
            data:
              type: object
    """
    response_data = {}
    response_data['status'] = True
    response_data['message'] =  ''
    response_data['data'] = {"txt":"Hello {0}".format(args['name'])} 
    
    print(args['type'], args['name'])
    return api_response(response_data), 200