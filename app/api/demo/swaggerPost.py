
from lib.utils import api_response
from ..route import api_route
from datetime import datetime   
from lib.cacheUtils import cache


req_params = {}
req_params['name'] = ['']
req_params['type'] = ['']
@api_route(rule = '', params=req_params ,methods=['POST'])
def _swaggerPost(args):
    """
    Create a new item
    ---
    tags:
      - Items
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - type
          properties:
            name:
              type: string
              description: The name of the item
            type:
              type: string
              description: The type of the item
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