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
    res = extract_info(text_result)
    return json({
        "state": "sucesss",
        "data": res
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