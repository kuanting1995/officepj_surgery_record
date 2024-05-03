import requests
import json
from datetime import datetime


# 檢驗檢查 Details表格

def format_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y%m%d')
    return datetime.strftime(date_obj, '%m/%d')

def makeFlexMsg_LabDetails(patname, category, lab_details):

    formatted_date_0 = format_date(lab_details['latest_4_dates'][0])
    formatted_date_1 = format_date(lab_details['latest_4_dates'][1])
    formatted_date_2 = format_date(lab_details['latest_4_dates'][2])
    formatted_date_3 = format_date(lab_details['latest_4_dates'][3])
    
    msg = {
        "type": "flex",
        "contents": {
            "body": [
                {
                    "type": "bodycontainer",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"病人:{patname} 檢驗檢查 {category}",
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
                            "text": "item",
                            "align": "left",
                            "fontColor": "#373737",
                            "fontSize": 15,
                            "fontStyle": "normal",
                            "fontWeight": 400,
                            "marginTop": 10
                        },
                         {
                            "type": "text",
                            "text": formatted_date_3,
                            "align": "center",
                            "fontColor": "#373737",
                            "fontSize": 15,
                            "fontStyle": "normal",
                            "fontWeight": 400,
                            "marginTop": 10
                        },
                        {
                            "type": "text",
                            "text": formatted_date_2,
                            "align": "center",
                            "fontColor": "#373737",
                            "fontSize": 15,
                            "fontStyle": "normal",
                            "fontWeight": 400,
                            "marginTop": 10
                        },
                        {
                            "type": "text",
                            "text": formatted_date_1,
                            "align": "center",
                            "fontColor": "#373737",
                            "fontSize": 15,
                            "fontStyle": "normal",
                            "fontWeight": 400,
                            "marginTop": 10
                        },
                        {
                            "type": "text",
                            "text": formatted_date_0,
                            "align": "center",
                            "fontColor": "#373737",
                            "fontSize": 15,
                            "fontStyle": "normal",
                            "fontWeight": 400,
                            "marginTop": 10
                        }
                    ],
                    "borderColor": "#DCDCDC",
                    "borderWidth": 1,
                    "paddingStart": 10,
                    "paddingEnd": 10
                }
            ]
        }
    }

    for item in lab_details['result_data'][:28]:
        # print('item', item)
        new_container = {
            "type": "bodycontainer",
            "contents": [
                {
                    "type": "text",
                    "text": item['name'],
                    "align": "left",
                    "fontColor": "#373737",
                    "fontSize": 15,
                    "fontStyle": "normal",
                    "fontWeight": 400,
                    "marginTop": 10
                },
                {
                    "type": "text",
                    "text":  item.get(lab_details['latest_4_dates'][3], ""),
                    "align": "center",
                    "fontColor": "#373737",
                    "fontSize": 15,
                    "fontStyle": "normal",
                    "fontWeight": 400,
                    "marginTop": 10
                },
                {
                    "type": "text",
                    "text":  item.get(lab_details['latest_4_dates'][2], ""),
                    "align": "center",
                    "fontColor": "#373737",
                    "fontSize": 15,
                    "fontStyle": "normal",
                    "fontWeight": 400,
                    "marginTop": 10
                },
                  {
                    "type": "text",
                    "text":  item.get(lab_details['latest_4_dates'][1], ""),
                    "align": "center",
                    "fontColor": "#373737",
                    "fontSize": 15,
                    "fontStyle": "normal",
                    "fontWeight": 400,
                    "marginTop": 10
                },
                  {
                    "type": "text",
                    "text":  item.get(lab_details['latest_4_dates'][0], ""),
                    "align": "center",
                    "fontColor": "#373737",
                    "fontSize": 15,
                    "fontStyle": "normal",
                    "fontWeight": 400,
                    # "bgcolor": "#b5b398",
		            "marginTop": 10
                }
            ],
            "borderColor": "#DCDCDC",
            "borderWidth": 1,
            "paddingStart": 10,
            "paddingEnd": 10
        }
        
        msg['contents']['body'].append(new_container)

    return msg





# 檢驗檢查 日期+分類按鈕
# {"B": "#DCDCDC","C": "#C0F7A4","E": "#FDF6C0","eC": "#FDF6C0", "H": "#FFCDD2","I": "#B3E5FC","IM": "#B3E5FC","M": "#FFFAFA","S": "#D8B598","T": "#F5DEB3","U": "#F0E68C","D": "#FFFAFA"} 
# 重整labdata格式:1.sys_date日期改為04/29格式 2.tests E改為=>eC,I=>IM 3.加入對應色彩color_mapping
def reformat_data(lab_details):
    color_mapping = {"B": "#DCDCDC","C": "#C0F7A4","E": "#FDF6C0","eC": "#FDF6C0", "H": "#FFCDD2","I": "#B3E5FC","IM": "#B3E5FC","M": "#FFFAFA","S": "#D8B598","T": "#F5DEB3","U": "#F0E68C","D": "#FFFAFA"}
    result = []
    for data in lab_details:
        sys_date = datetime.strptime(data["SYS_DATE"], '%Y%m%d').strftime('%m/%d')
        original_tests = [key for key in data.keys() if key != "SYS_DATE"]
        tests = [key if key != 'E' and key != 'I' else 'eC' if key == 'E' else 'IM' for key in original_tests]
        tests_with_color = {tests[i]: str(data[original_tests[i]]) + ', ' + color_mapping.get(original_tests[i], "#colorcode") for i in range(len(tests))} 
        result.append({"date": sys_date, "org_sys_date": data["SYS_DATE"],"tests": tests_with_color})
    return result
def makeFlexMsg_Lab(patname,lab_details,_id):
    formatted_data = reformat_data(lab_details)
    
    msg = {
        "type": "flex",
        "contents": {
            "body": [
                {
                    "type": "bodycontainer",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"病人:{patname}   檢驗檢查 (最新5筆)",
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
                }
            ],
            "footer": []
        }
    }

    counter = 0
    for entry in formatted_data:
        tests = list(entry["tests"].keys())
        containers = []
        isFirstContainer = True  # move the flag inside the outer loop

        while tests:
            container_tests = tests[:3]
            tests = tests[3:]

            # calculate paddingEnd (considering both messagebutton and postbackbutton)
            total_buttons = len(container_tests) + 1
            if total_buttons == 1:
                paddingEnd = 252
            elif total_buttons == 2:
                paddingEnd = 175
            elif total_buttons == 3:
                paddingEnd = 107
            else:  # total_buttons == 4
                paddingEnd = 40
                
            container = {
                "type": "footercontainer",
                "contents": [],
                "borderColor": "#DCDCDC",
                "paddingStart": 10,
                "paddingEnd": paddingEnd
            }

            # if it's the first container, display the date, otherwise display empty
            date_text = entry["date"] if isFirstContainer else " "
            isFirstContainer = False  # update the flag
   
            container["contents"].append({
                "type": "messagebutton",
                "text": date_text,
                "style": "secondary",
                "fontColor": "#373737",
                "message": "N/A"
            })

            for test in container_tests:
                counter += 1
                test_color = entry["tests"][test].split(', ')[1]
                # test_value = entry["tests"][test].split(', ')[0]
                org_sys_date = entry["org_sys_date"]
                container["contents"].append({
                    "type": "postbackbutton",
                    "text": f"{test}",
                    # "text": f"{test} /{test_value}",
                    "style": "primary",
                    "fontColor": "#373737",
                    "bgcolor": test_color,
                    "displayText": '已查詢檢驗檢查',
                    "data": f"value={20+counter}&id={_id}&categorty={test}&date={org_sys_date}"
                })

            containers.append(container)
        
        msg["contents"]["footer"].extend(containers)

    return msg

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
						"text": f"病人:{patname}   生命徵象(7days)",
						"align": "left",
						"fontColor": "#373737",
						"fontSize": 18,
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
						"text": "查詢active order:",
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
						"text": "查詢active order:",
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
			},
			{
				"type": "footercontainer",
				"contents": [
					{
						"type": "postbackbutton",
						"text": "生命徵象",
						"style": "primary",
      					"bgcolor":"#b5989a",
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
						"bgcolor":"#b5b398",
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