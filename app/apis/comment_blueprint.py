from sanic import Blueprint
from sanic.response import json
from app.databases.mongodb import MongoDB

comment_blueprint = Blueprint('comment', url_prefix='/comment')

_db = MongoDB()

@comment_blueprint.route('/create', methods={'POST'})
async def create_comment(request):
    try :
        res = _db.create_feedback(request.json['img_url'], request.json['username'], request.json['point'], request.json['data'], request.json['comment'])
        return json({
            'status': res,
        })
    except:
        return json({
            'status': 'false',
        })

@comment_blueprint.route('/count', methods={'POST'})
async def count_comment(request):
    try :
        res = _db.count_comments()
        return json({
            'status': 'success',
            "data": res
        })
    except:
        return json({
            'status': 'false',
        })
    
@comment_blueprint.route('/point', methods={'POST'})
async def average_point(request):
    try :
        res = _db.average_points_all_comments()
        return json({
            'status': 'success',
            "data": res
        })
    except:
        return json({
            'status': 'false',
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