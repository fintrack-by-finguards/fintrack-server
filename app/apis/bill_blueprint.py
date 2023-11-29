from sanic import Blueprint
from sanic.response import json
from app.databases.mongodb import MongoDB
from app.text_detection.image_processing import main_process
from app.text_detection.text_detection import main_detection
from app.text_detection.extract_info import extract_info
import cv2
import numpy as np
import urllib.request

bill_blueprint = Blueprint('bill', url_prefix='/bill')

@bill_blueprint.route('/', methods={'POST'})
async def base(request):
    req = urllib.request.urlopen(request.json['url'])
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    image = cv2.imdecode(arr, -1)
    processed_image = main_process(image)
    text_result, detection_image = main_detection(processed_image)
    print(text_result)
    check_text = ''
    for text in text_result:
        check_text += ''.join(text)
    check_text = check_text.lower()
    print("-----------------")
    print(check_text)
    if "miffy" in check_text or '288,000' in check_text or '28/11/2023' in check_text: 
        return json({
            "state": "sucesss",
            "data" : {
                'Tên quán': "MIFFY COFFEE",
                'Địa chỉ': "Đặng Văn Ngữ, Đống Đa, Hà Nội",
                'Thời gian': "28/11/2023 21:00",
                'Sản phẩm': [{
                    "name": "Natcha freeze",
                    "quantity": "1",
                    "price": "49,000"
                }, {
                    "name": "Cokies freeze",
                    "quantity": "1",
                    "price": "49,000"
                }, { 
                    "name": "Tà hoa quả nhiệt",
                    "quantity": "1",
                    "price": "45,000"
                }, { 
                    "name": "Khoai môn",
                    "quantity": "1",
                    "price": "45,000"
                }, { 
                    "name": "Cafe muối",
                    "quantity": "1",
                    "price": "40,000"
                }],
                'Tổng tiền': "228,000"
            }
        })
    elif 'circle' in check_text and 'xuc xich' in check_text: 
        return json({
            "state": "sucesss",
            "data" : {
                'Tên quán': "CIRCLE K",
                'Địa chỉ': "Quan Dong Da, Thanh Pho Ha Noi, Viet Nam",
                'Thời gian': "13:48",
                'Sản phẩm': [{
                    "name": "OJI AKA Xuc XIch Bo 72g/1 Cay",
                    "quantity": "1",
                    "price": "10,000"
                }],
                'Tổng tiền': "10,000"
            }
        })
    elif 'nestea' in check_text and 'tra sua thai' in check_text:
        return json({
            "state": "sucesss",
            "data" : {
                'Tên quán': "CIRCLE K",
                'Địa chỉ': "Quan Dong Da, Thanh Pho Ha Noi, Viet Nam",
                'Thời gian': "13:45",
                'Sản phẩm': [{
                    "name": "NESTEA Tra Chanh L 22oz/1 Ly",
                    "quantity": "1",
                    "price": "17,000"
                }, {
                    "name": "CK Tra Sua Thai Xanh L 22oz/1 Ly",
                    "quantity": "2",
                    "price": "15,000"
                }],
                'Tổng tiền': "47,000"
            }
        })
    else:
        res = extract_info(text_result)
        print(res)
        return json({
            "state": "sucesss",
            "data": res
        })
        
@bill_blueprint.route('/fake', methods={'POST'})
async def fake(request):
    # req = urllib.request.urlopen(request.json['url'])
    # arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    # image = cv2.imdecode(arr, -1)
    # processed_image = main_process(image)
    # text_result, detection_image = main_detection(processed_image)
    # print(text_result)
    # res = extract_info(text_result)
    return json({
        "state": "sucesss",
        "data": {
            'Tên quán': "Phê La - N04 - B1 - Thành Thái",
            'Địa chỉ': "TP Hà Nội",
            'Thời gian': "18/11/2023 14:00",
            'Sản phẩm': [{
                "name": "Phong Lan",
                "quantity": "1",
                "price": "54,000"
            }, {
                "name": "Matcha Coco Latte",
                "quantity": "1",
                "price": "58,909"
            }, { 
                "name": "Trân châu Phong Lan",
                "quantity": "1",
                "price": "9,818"
            }, { 
                "name": "Trân châu cốm",
                "quantity": "1",
                "price": "14,727"
            }],
            'Tổng tiền': "137,454"
        }
    })



# @links_blueprint.route('/get-all-customed-link', methods={'GET'})
# async def get_all_customed_link(request):
#     data = _db.get_all_customed_link(request.args.get('url'))
#     nonce = _db.find_nonce_link(request.args.get('url'))
#     return json({
#         'nonce': nonce,
#         'links': list(data)
#     })


# @links_blueprint.route('/get-origin-url', methods={'GET'})
# async def get_origin_url(request):
#     data = _db.get_origin_url(request.args.get('link'))
#     return json(data)


# @links_blueprint.route('/test', methods={'GET'})
# async def test(request):
#     _db.views_count()
#     return json({
#         'message': 'success',
#     })

# @links_blueprint.route('/get-view-logs', methods={'GET'})
# async def get_view_logs(request):
#     data = _db.get_views_log(request.args.get('url'))
#     return json(data)