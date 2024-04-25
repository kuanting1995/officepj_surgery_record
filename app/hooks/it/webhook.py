
from flask import Flask, request, jsonify
import requests
from ..route import api_route 
from  settings import Config
from lib.Checker import isNone
import uuid
from urllib.parse import parse_qs
from datetime import datetime
from lib.logger import logger


CHANNEL_ACCESS_TOKEN = Config.IT_CHANNEL_ACCESS_TOKEN

@api_route(rule = '', params=None ,methods=['POST', 'GET'])
def _webhook():
    if not request.data:
        return "Webhook received!"

    return not request.data
