
from datetime import datetime
from settings import Config, ReverseProxied
from flask import Flask
from flask_cors import CORS
from lib.logger import logger
from lib import utils
from lib.cacheUtils import initial_cache
import requests
from flasgger import Swagger

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'DEFAULT@SECLEVEL=0'

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app, script_name=Config.APPLICATION_ROOT)

# Config
app.config.from_object(Config)

app.config['SWAGGER'] = {
    'base_url': Config.APPLICATION_ROOT,  # 设置 Swagger UI 的基础 URL
}

swagger =  Swagger(app, config={
    'headers': [],
    'specs': [
        {
            'endpoint': 'apispec_1',
            'route': '/apispec_1.json',
            'rule_filter': lambda rule: True,  # 所有规则
            'model_filter': lambda tag: True,  # 所有模型
        }
    ],
    'static_url_path': '/flasgger_static',
    'swagger_ui': True,
    'specs_route': '/apidocs/',
    "basePath": Config.APPLICATION_ROOT,  # 指定 API 的基本路径,
})




def initialize_route(flask_app):
    logger.info('initialize routes ...')
    
    from api.route import apiprint as api_print , prefix as api_prefix
    flask_app.register_blueprint(
        api_print, url_prefix='/{0}'.format(api_prefix))
    
    from hooks.route import apiprint as hooks_print , prefix as hooks_prefix
    flask_app.register_blueprint(
        hooks_print, url_prefix='/{0}'.format(hooks_prefix))    


@app.teardown_appcontext
def shutdown_session(exception=None):
    # db_session.remove()
    # pg_session.remove()
    # ora_session.remove()
    pass



@app.route('/')
def api_index():
    """所有API列表"""
    from api.route import route_info
    return route_info(None)


def initial_app():
    CORS(app) # Cross-Origin Resource Sharing
    initial_cache(app) 
    initialize_route(app)
    logger.info(' Listening at: http://localhost:5000')

if __name__ != "__main__":
    initial_app()

if __name__ == '__main__':
    initial_app()
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)
   



