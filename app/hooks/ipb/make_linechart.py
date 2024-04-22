import json
import subprocess
import os
import tempfile
from datetime import datetime
import requests
import json
from settings import Config

"""
帶入data生成linechart image
使用python內建套件subprocess執行highchart-server功能,須先載nodejs和 npm highchart-server
highchart-server未提供圖片binary,要先用tempfile存並轉binary,再轉成base64才能用json格式傳送
"""

def create_VitalSignChart(data):

    # 格式日期不要年份 04/15 12:00
    formatted_dates = [datetime.strptime(item["datetime"], "%Y/%m/%d %H:%M").strftime("%m/%d %H:%M") for item in data]
    # print('formatted_dates',formatted_dates)
    # 血壓資料 組成區域色塊數據[(111,80)...]
    SBP_DATA = [item["BPS"] for item in data]
    DBP_DATA = [item["BPD"] for item in data]
    SBPcombinedDBP = [[item1, item2] for item1, item2 in zip(SBP_DATA, DBP_DATA)]
    
    # 生成 Highcharts 配置
    options = {
    "chart": {
        "width": 950  # 調整此數值以改變圖表寬度
    },
    "title": {
        "text": "vital sign",
        "style": {
            "color": "#666666", 
            "fontSize": "14px"
        }
    },
    "xAxis": {
        "categories": formatted_dates,
        "title": {
            "text": ""
        },
        "labels": {
            "style": {
                "fontSize": "9px"
            }
        }
    },
    "yAxis": {
        "title": {
            "text": ""
        },
        "labels": {
            "style": {
                "fontSize": "10px"
            }
        }
    },
    "exporting": {
        "scale": 20
    },
    "legend": {
        "itemStyle": {
            "fontSize": "8px"
        }
    },
    "series": [
        {
            "type": "line",
            "data": [item["TEMP"] for item in data],
            "name": "Temp(˚C)",
            "color": "#3366ff",
            "marker": {
                "symbol": "circle",
                "radius": 2
            },
            "dataLabels": {
                "enabled": True,
                "format": "{y}",
                "color": "#3366ff",
                "align": "right",
                "x": 10,
                "y": 15,
                "style": {
                    "fontSize": '6px'
                }
            }
        }, 
        {
            "type": "line",
            "data": [item["PULSE"] for item in data],
            "name": "Pulse (bpm)",
            "color": "#db2143",
            "marker": {
                "symbol": "diamond",
                "radius": 2
            },
            "dataLabels": {
                "enabled": True,
                "format": "{y}",
                "color": "#db2143",
                "align": "right",
                "x": 10,
                "style": {
                    "fontSize": '6px'
                }
            }
        }, 
        {
            "type": "line",
            "data": [item["RESP"] for item in data],
            "name": "Resp(/min)",
            "color": "#373737",
            "marker": {
                "symbol": "triangle",
                "radius": 2
            },
            "dataLabels": {
                "enabled": True,
                "format": "{y}",
                "color": "#373737",
                "align": "right",
                "x": 10,
                "y": 15,
                "textOutline": "none",
                "style": {
                    "fontSize": '6px'
                }
            }
        }, 
        {
            "type": "line",
            "data": SBP_DATA,
            "name": "SBP(mmHg)",
            "color": "#3d7b3d",
            "lineWidth": 0,
            "marker": {
                "symbol": "triangle-down",
                "radius": 2
            },
            "dataLabels": {
                "enabled": True,
                "format": "{y}",
                "color": "#3d7b3d",
                "align": "right",
                "x": 10,
                "y": -17,
                "textOutline": "none",
                "style": {
                    "fontSize": '6px'
                }
            }
        }, 
        {
            "type": "line",
            "data": DBP_DATA,
            "name": "DBP(mmHg)",
            "color": "#3d7b3d",
            "lineWidth": 0,
            "marker": {
                "symbol": "triangle",
                "radius": 2
            },
            "dataLabels": {
                "enabled": True,
                "format": "{y}",
                "color": "#3d7b3d",
                "align": "right",
                "x": 10,
                "y": 13,
                "textOutline": "none",
                "style": {
                    "fontSize": '6px'
                }
            }
        },
        {
            "type": "arearange",
            "data": SBPcombinedDBP,
            "color": "#04b404",
            "fillColor": "rgba(4, 180, 4, 0.1)",
            "lineWidth": 0,
            "marker": {
                "enabled": False
            },
            "enableMouseTracking": False,
            "showInLegend": False # 隱藏最下方圖例

        }]
    }
            
    # Highcharts Export Server URL
    
    url = "{0}/export".format(Config.HIGHCHARTS_SERVER)
    # 发送 POST 请求到 Export Server
    response = requests.post(url, json={"options": options, "type": "png"}, timeout=(5, 30))     
  
    if response.status_code == 200:
        return response.content
    else:
        return b""

 



# 生成图表
# create_chart()
# import datetime
# now = datetime.datetime.now()
# output_file = "/home/dev/folder/linechart_{:%Y_%m_%d_%H_%M_%S}.png".format(now) 存在mongodb....?
# create_chart(x_categories, data_temp, data_pulse, data_resp, data_sbp, data_dbp, data_arearange, output_file)