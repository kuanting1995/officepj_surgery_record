import requests
import json
from datetime import datetime


# 生命徵象折線圖
def makeFlexMsg_VitalSignChart(patname,imageid):
    
    msg = {
	"type": "flex",
	"contents": {
		"body": [
			{
				"type": "bodycontainer",
				"contents": [
					{
						"type": "text",
						"text": f"病人{patname} 生命徵象(7days)",
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 16,
						"fontStyle": "normal",
						"fontWeight": 900,
						"marginTop": 5
					}
				],
				"borderColor": "#DCDCDC",
				"paddingBottom": 20,
				"paddingStart": 10,
				"paddingEnd": 10
			},
			{
				"type": "bodycontainer",
				"contents": [
					{
						"type": "image",
						"id": imageid['FileID'],
						"aspectRatio": "7:3",
    #   ***w950 7：3, w900 9:4
						"scaleType": "fit"
					}
				],
				"borderColor": "#DCDCDC",
				"paddingStart": 10,
				"paddingEnd": 10
			}
		]
	}
}
    return msg

# 製作分類過的active order列表
def makeFlexMsg_OrderDetails(patname,bedno,ordertype_value ,data):
    msg = {
	"type": "flex",
	"contents": {
		"body": [
			{
				"type": "bodycontainer",
				"contents": [
					{
						"type": "text",
						"text": f"病人:{patname} ",
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 18,
						"fontStyle": "normal",
						"fontWeight": 900,
						"marginTop": 5
					},
					{
						"type": "text",
						"text": f"床號:{bedno}",
						"align": "right",
						"fontColor": "#373737",
						"fontSize": 16,
						"fontStyle": "normal",
						"fontWeight": 600,
						"marginTop": 5
					}
				],
				"borderColor": "#DCDCDC",
				"paddingStart": 10,
				"paddingEnd": 10
			},
			{
				"type": "bodycontainer",
				"contents": [
					{
						"type": "text",
						"text": f"< {ordertype_value} active order >",
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 18,
						"fontStyle": "normal",
						"fontWeight": 900,
						"marginTop": 10
					}
				],
				"borderColor": "#DCDCDC",
				"paddingTop": 0,
				"paddingBottom": 0,
				"paddingStart": 10,
				"paddingEnd": 10
			},
			{
				"type": "separator",
				"height": 1,
				"bgcolor": "#DCDCDC"
			}
		]
	}
}
    # 將active_order_data 先做日期排序：
    sorted_orders = sorted(data , key=lambda order: order["BeginDateTimeStr"], reverse=True)
    for order_data in sorted_orders:
        date_container = {
            "type": "bodycontainer",
            "contents": [
                {
                    "type": "text",
                    "text": "日期:",
                    "align": "left",
                    "fontColor": "#373737",
                    "fontSize": 15,
                    "fontStyle": "normal",
                    "fontWeight": 400,
                    "marginTop": 10
                },
                {
                    "type": "text",
                    "text": order_data["BeginDateTimeStr"],
                    "flex": 3,
                    "align": "left",
                    "fontColor": "#373737",
                    "fontSize": 15,
                    "fontStyle": "normal",
                    "fontWeight": 400,
                    "marginTop": 10
                }
            ],
            "borderColor": "#DCDCDC",
            "paddingStart": 10,
            "paddingEnd": 10
        }

        text_container = {
            "type": "bodycontainer",
            "contents": [
                {
                    "type": "text",
                    "text": "orddtxt:",
                    "align": "left",
                    "fontColor": "#373737",
                    "fontSize": 15,
                    "fontStyle": "normal",
                    "fontWeight": 400,
                    "marginTop": 10
                },
                {
                    "type": "text",
                    "text": order_data["OrddTxt"],
                    "flex": 3,
                    "align": "left",
                    "fontColor": "#373737",
                    "fontSize": 15,
                    "fontStyle": "normal",
                    "fontWeight": 400,
                    "marginTop": 10
                }
            ],
            "bgcolor": "#bdc9d4",
            "borderColor": "#DCDCDC",
            "paddingStart": 10,
            "paddingEnd": 10
        }

        msg['contents']['body'].extend([date_container, text_container])

    return msg

# active order分類按鈕 x8
def makeFlexMsg_CategoryOrder(_id,obj):
    msg = {
        "type": "flex",
        "contents": {
            "body": [
			{
				"type": "bodycontainer",
				"contents": [
					{
						"type": "text",
						"text": "病人" + obj['obj']['PAT_NAME'],
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 18,
						"fontStyle": "normal",
						"fontWeight": 900,
						"marginTop": 10
					}
				],
				"borderColor": "#DCDCDC",
				"paddingStart": 10,
				"paddingEnd": 10
			},
			{
				"type": "bodycontainer",
				"contents": [
					{
						"type": "text",
						"text": "分類查詢active order:",
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 16,
						"fontStyle": "normal",
						"fontWeight": 600,
						"marginTop": 10
					}
				],
				"borderColor": "#DCDCDC",
				"paddingTop": 0,
				"paddingBottom": 0,
				"paddingStart": 10,
				"paddingEnd": 10
			},
			{
				"type": "separator",
				"height": 1,
				"bgcolor": "#DCDCDC"
			}
		],
            "footer": [
			{
				"type": "footercontainer",
				"contents": [
					{
						"type": "postbackbutton",
						"text": "點滴/針劑",
						"style": "primary",
						"bgcolor": "#2C5062",
                        "displayText": '已查詢"點滴/針劑"active order',
                        "data": "value=3&id="+_id
					},
					{
						"type": "postbackbutton",
						"text": "口服/外用",
						"style": "primary",
						"bgcolor": "#99AAB6",
                        "displayText": '已查詢"口服/外用"active order',
                        "data": "value=4&id="+_id
					},
					{
						"type": "postbackbutton",
						"text": "醫療指示",
						"style": "primary",
						"bgcolor": "#6A8391",
                        "displayText": '已查詢"醫療指示"active order',
                        "data": "value=5&id="+_id
					}
				],
				"borderColor": "#DCDCDC",
				"paddingStart": 10,
				"paddingEnd": 10
			},
			{
				"type": "footercontainer",
				"contents": [
					{
						"type": "postbackbutton",
						"text": "檢驗檢查",
						"style": "primary",
						"bgcolor": "#6A8391",
                        "displayText": '已查詢"檢驗檢查"active order',
                        "data": "value=6&id="+_id
					},
					{
						"type": "postbackbutton",
						"text": "化療",
						"style": "primary",
						"bgcolor": "#2C5062",
                        "displayText": '已查詢"化療"active order',
                        "data": "value=7&id="+_id
					}
				],
				"borderColor": "#DCDCDC",
				"paddingStart": 10,
				"paddingEnd": 10
			},
   			{
				"type": "footercontainer",
				"contents": [
					{
						"type": "postbackbutton",
						"text": "PCA",
						"style": "primary",
						"bgcolor": "#2C5062",
                        "displayText": '已查詢"PCA"active order',
                        "data": "value=8&id="+_id
					},
					{
						"type": "postbackbutton",
						"text": "出院醫囑",
						"style": "primary",
						"bgcolor": "#99AAB6",
                        "displayText": '已查詢"出院醫囑"active order',
                        "data": "value=9&id="+_id
					},
					{
						"type": "postbackbutton",
						"text": "全部",
						"style": "primary",
						"bgcolor": "#6A8391",
                        "displayText": '已查詢"全部"active order',
                        "data": "value=10&id="+_id
					}
				],
				"borderColor": "#DCDCDC",
				"paddingStart": 10,
				"paddingEnd": 10
			}
		]
        }
    }
    return msg


# 病人基本資料+ 查詢按鈕 x3
def makeFlexMsg_PatBaseInfo(_id,data):
    patName = data['PAT_NAME'] 
    charNo = data['CHART_NO']
    patidNo = data['PAT_IDNO']
    sex = data['SEX']
    sex = '男' if sex == 'M' else '女' if sex == 'F' else '未知'
    nowstation = data['NOW_STATIONNO']
    nowbedno = data['NOW_BEDNO']
    docname = data['DOC_NAME1']
    nursename = data['DOC_NAME2'] if(data['DOC_NAME2']) else " "
    msg = {
	"type": "flex",
	"contents": {
		"body": [
			{
				"type": "bodycontainer",
				"contents": [
					{
						"type": "text",
						"text": "病人基本資料",
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 18,
						"fontStyle": "normal",
						"fontWeight": 900,
						"marginTop": 10
					}
				],
				"borderColor": "#DCDCDC",
				"paddingStart": 10,
				"paddingEnd": 10
			},
			{
				"type": "separator",
				"height": 1,
				"bgcolor": "#DCDCDC"
			},
			{
				"type": "bodycontainer",
				"contents": [
					{
						"type": "text",
						"text": "病人",
						"flex": 3,
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontStyle": "normal",
						"fontWeight": 400,
						"marginTop": 10
					},
					{
						"type": "text",
						"text": patName,
						"flex": 4,
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontStyle": "normal",
						"fontWeight": 400,
						"marginTop": 10
					}
				],
				"borderColor": "#DCDCDC",
				"paddingStart": 10,
				"paddingEnd": 10
			},
			{
				"type": "bodycontainer",
				"contents": [
					{
						"type": "text",
						"text": "病例號",
						"flex": 3,
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontStyle": "normal",
						"fontWeight": 400,
						"marginTop": 10
					},
					{
						"type": "text",
						"text": charNo,
						"flex": 4,
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontStyle": "normal",
						"fontWeight": 400,
						"marginTop": 10
					}
				],
				"borderColor": "#DCDCDC",
				"paddingStart": 10,
				"paddingEnd": 10
			},
			{
				"type": "bodycontainer",
				"contents": [
					{
						"type": "text",
						"text": "身份證",
						"flex": 3,
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontStyle": "normal",
						"fontWeight": 400,
						"marginTop": 10
					},
					{
						"type": "text",
						"text": patidNo,
						"flex": 4,
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontStyle": "normal",
						"fontWeight": 400,
						"marginTop": 10
					}
				],
				"borderColor": "#DCDCDC",
				"paddingStart": 10,
				"paddingEnd": 10
			},
			{
				"type": "bodycontainer",
				"contents": [
					{
						"type": "text",
						"text": "性別",
						"flex": 3,
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontStyle": "normal",
						"fontWeight": 400,
						"marginTop": 10
					},
					{
						"type": "text",
						"text": sex,
						"flex": 4,
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontStyle": "normal",
						"fontWeight": 400,
						"marginTop": 10
					}
				],
				"borderColor": "#DCDCDC",
				"paddingStart": 10,
				"paddingEnd": 10
			},
   			{
				"type": "bodycontainer",
				"contents": [
					{
						"type": "text",
						"text": "護理站-床號",
						"flex": 3,
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontStyle": "normal",
						"fontWeight": 400,
						"marginTop": 10
					},
					{
						"type": "text",
						"text":  f"{nowstation}-{nowbedno}",
						"flex": 4,
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontStyle": "normal",
						"fontWeight": 400,
						"marginTop": 10
					}
				],
				"borderColor": "#DCDCDC",
				"paddingStart": 10,
				"paddingEnd": 10
			},
   			{
				"type": "bodycontainer",
				"contents": [
					{
						"type": "text",
						"text": "主治醫師",
						"flex": 3,
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontStyle": "normal",
						"fontWeight": 400,
						"marginTop": 10
					},
					{
						"type": "text",
						"text": docname,
						"flex": 4,
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontStyle": "normal",
						"fontWeight": 400,
						"marginTop": 10
					}
				],
				"borderColor": "#DCDCDC",
				"paddingStart": 10,
				"paddingEnd": 10
			},
   			{
				"type": "bodycontainer",
				"contents": [
					{
						"type": "text",
						"text": "專科護理師",
						"flex": 3,
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontStyle": "normal",
						"fontWeight": 400,
						"marginTop": 10
					},
					{
						"type": "text",
						"text": nursename,
						"flex": 4,
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 15,
						"fontStyle": "normal",
						"fontWeight": 400,
						"marginTop": 10
					}
				],
				"borderColor": "#DCDCDC",
				"paddingStart": 10,
				"paddingEnd": 10
			}
		],
		"footer": [
			{
				"type": "footercontainer",
				"contents": [
					{
						"type": "postbackbutton",
						"text": "查詢active order",
						"style": "primary",
						"displayText": "您已查詢active order",
                        "data": "value=0&id="+_id
					}
				],
				"borderColor": "#DCDCDC",
				"paddingStart": 10,
				"paddingEnd": 10
			},
			{
				"type": "footercontainer",
				"contents": [
					{
						"type": "postbackbutton",
						"text": "生命徵象",
						"style": "primary",
                        "displayText": "您已查詢生命徵象,圖表產製中...",
                        "data": "value=1&id="+_id
					}
				],
				"borderColor": "#DCDCDC",
				"paddingStart": 10,
				"paddingEnd": 10
			},
			{
				"type": "footercontainer",
				"contents": [
					{
						"type": "postbackbutton",
						"text": "檢驗檢查",
						"style": "primary",
                        "displayText": "您已查詢檢驗檢查",
                        "data": "value=2&id="+_id
					}
				],
				"borderColor": "#DCDCDC",
				"paddingStart": 10,
				"paddingEnd": 10
			}
		]
	}
}
    return msg



# if __name__=="__main__":
#     x = makeFlexMsgForUser("林OO", "20230424")
#     print(json.dumps(x))