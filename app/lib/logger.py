import logging
from settings import RequestFormatter
from logging.handlers import SysLogHandler
from logging import FileHandler
from settings import Config

logger = logging.getLogger('gunicorn.error')

# 定义一个检查处理器是否存在的函数
def handler_exists(logger, handler_type):
    return any(isinstance(handler, handler_type) for handler in logger.handlers)

if(not Config.DEBUG):
    if not handler_exists(logger, SysLogHandler):  # 检查是否已经有处理器，避免重复添加
        handler = SysLogHandler((Config.SYSLOG_URL, int(Config.SYSLOG_PORT)),)
        formatter = RequestFormatter(
            '[%(app_name)s] [%(process)s] [%(asctime)s] %(remote_addr)s requested %(url)s\n'
            '%(levelname)s in %(module)s: %(message)s'
        )
        handler.setFormatter(formatter)
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        
        
else:
    if not handler_exists(logger, logging.FileHandler):  # 检查是否已经有处理器，避免重复添加
        logger = logging.getLogger("gunicorn.error")
        handler = FileHandler('./log/debug/flask.log')
        formatter = RequestFormatter(
            '[%(app_name)s] [%(asctime)s] %(remote_addr)s requested %(url)s\n'
            '%(levelname)s in %(module)s: %(message)s'
        )
        handler.setFormatter(formatter) 
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
