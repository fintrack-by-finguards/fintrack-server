from sanic import Blueprint
from sanic.response import json
from app.databases.mongodb import MongoDB

user_blueprint = Blueprint('user', url_prefix='/user')

_db = MongoDB()

@user_blueprint.route('/', methods={'GET'})
async def base(request):
    return json({
        "message": "User"
    })
    

@user_blueprint.route('/create', methods={'POST'})
async def create_user(request):
    try :
        res = _db.create_user(request.json['username'], request.json['password'], request.json['name'], request.json['birthday'], request.json['job'], request.json['university'])
        return res
    except:
        return json({
            'status': 'false',
        })
    
@user_blueprint.route('/getOne', methods={'POST'})
async def get_user(request):
    try :
        data = _db.get_user(request.json['username'])
        return json({
            'status': 'success',
            'data': data
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