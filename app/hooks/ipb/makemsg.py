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
def makeFlexMsg_OrderDetails(patname, bedno, majorname, activeorder_by_type):
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
                            "text": f"< {majorname} active order >",
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
    
    def get_datetime_str(order):
        # print(order)
        beg_datetime = datetime.strptime(order['BEG_DATE'] + order['BEG_TIME'] + '00', '%Y/%m/%d%H%M%S')
        return beg_datetime.strftime('%Y-%m-%d %H:%M')

    sorted_orders = sorted(activeorder_by_type, key=get_datetime_str,reverse=True)

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
                    "text": get_datetime_str(order_data),
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
                    "text": order_data["ORDD_TXT"],
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

# 最新執行 active order列表
def makeFlexMsg_OrderDetailsRecent(patname,bedno,ordertype_value ,data):
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
    current_year = datetime.now().year
    sorted_orders = sorted(data, key=lambda order: datetime.strptime(str(current_year) + "/" + order["BEG_ORDER"].split('\n')[0], '%Y/%m/%d %H:%M'),reverse=True)

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
                    "text":  str(current_year) + "/" + order_data["BEG_ORDER"].split('\n')[0],
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
                    "text": order_data["NAME_ORDER"],
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


# active order分類按鈕
def makeFlexMsg_CategoryOrder(_id, obj, Majorname_list):
    msg = {
        "type": "flex",
        "contents": {
            "body": [
                {
                    "type": "bodycontainer",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"病人{obj['PAT_NAME']} active order",
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
                            "text": "分類查詢:",
                            "align": "left",
                            "fontColor": "#373737",
                            "fontSize": 15,
                            "fontStyle": "normal",
                            "fontWeight": 500,
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
                }
            ],
            "footer": []
        }
    }

    for i, majorname in enumerate(Majorname_list, start=1):
        if i % 5 == 1:  # Start a new footercontainer every 5 items
            msg['contents']['footer'].append({
                "type": "footercontainer",
                "contents": [],
                "borderColor": "#DCDCDC",
                "paddingStart": 10,
                "paddingEnd": 10
            })

        msg['contents']['footer'][-1]['contents'].append({
            "type": "postbackbutton",
            "text": majorname,
            "style": "primary",
            "bgcolor": "#99AAB6",
            "displayText": f"您已查詢'{majorname}' active order",
            "data": f"value={i+2}&id={_id}"
        })

    # Add the special element to the last footercontainer
    msg['contents']['footer'].append({
        "type": "footercontainer",
        "contents": [{"type": "postbackbutton",
        "text": "最新執行",
        "style": "primary",
        "bgcolor": "#2C5062",
        "displayText": f'您已查詢"最新執行" active order',
        "data": f"value=20&id={_id}"}],
        "borderColor": "#DCDCDC",
		"paddingStart": 10,
		"paddingEnd": 10
    })

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
    nursename = data['DOC_NAME2']
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