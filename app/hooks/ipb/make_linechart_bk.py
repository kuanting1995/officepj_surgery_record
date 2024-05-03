import json
import subprocess
import os
import tempfile
from datetime import datetime
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
        "text": "生命徵象",
        "style": {
            "color": "#666666", 
            "fontSize": "14px"
        }
    },
    "subtitle": {
        "text": "vital sign",
        "style": {
            "color": "#666666", 
            "fontSize": "10px"
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
            
    # 創建臨時文件存取image binary, temp_fd檔案描述, temp_file檔案位置
    temp_fd, temp_file = tempfile.mkstemp()

    # 存取圖檔至 temp_file
    with open(temp_file, 'w') as f:
        json.dump(options, f)

    # 圖檔名稱：
    output_file = "linechart_{:%Y_%m_%d_%H_%M}.png".format(datetime.now())
    
    # 使用 highcharts-export-server 創建chart
    subprocess.run([
        "highcharts-export-server",
        "--infile", temp_file,
        "--type", "png",
        "--outfile", output_file
    ])
    # 讀取並存取 image_data (binary data-rb)
    with open(output_file, "rb") as f:
        image_data = f.read()
    
    # 刪除創建的圖片
    os.remove(output_file)

    # 關閉 file descriptor
    os.close(temp_fd)

    # 刪除 temporary file
    os.remove(temp_file)

    return image_data

