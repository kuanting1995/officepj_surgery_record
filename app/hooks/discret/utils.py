import os
import requests
from flask import Flask, request, jsonify
import uuid
import json
import time
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import base64
from  settings import Config

CHANNEL_ACCESS_TOKEN = Config.DISCRET_CHANNEL_ACCESS_TOKEN
MONDB_SERVER = 'https://emr.kfsyscc.org/mongo/teamplus_discret_channel'
def save_to_db(data, pgName):
    now = datetime.now()
    ts = datetime.timestamp(now)

    url = "{0}/requests".format(MONDB_SERVER)
    payload = {
        "_id": data["_id"],
        "mode":Config.APP_MODE,
        "progress_name": pgName,
        "req_datetime": ts,
        "review_datetime": ts,
        "messageSN": data["messageSN"],
        "rawdata":data
    }
    x = requests.post(url, json=payload)



def load_from_db(a_id):
    url = "{0}/requests/{1}".format(MONDB_SERVER, a_id)
    x = requests.get(url)
    return x.json()