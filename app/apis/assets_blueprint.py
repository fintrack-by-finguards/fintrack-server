from sanic import Blueprint
from sanic.response import json
from app.databases.mongodb import MongoDB

assets_blueprint = Blueprint('assets', url_prefix='/assets')

_db = MongoDB()

@assets_blueprint.route('/', methods={'GET'})
async def base(request):
    return json({
        "message": "Assets"
    })
    

@assets_blueprint.route('/update', methods={'POST'})
async def update_user_assets(request):
    try :
        res = _db.update_user_assets(request.json['username'], request.json['day'], request.json['month'], request.json['year']
                                     , request.json['assets'], request.json['debt'])
        return json({
            'status': res,
        })
    except:
        return json({
            'status': 'false',
        })
    
@assets_blueprint.route('/get', methods={'POST'})
async def get_user_assets(request):
    try :
        data = _db.get_user_assets(request.json['username'])
        return json({
            'status': 'success',
            'data': data
        })
    except:
        return json({
            'status': 'false',
        })
    

@assets_blueprint.route('/getOne', methods={'POST'})
async def get_user_assets_specific(request):
    try :
        data = _db.get_user_assets_specific(request.json['username'], request.json['day'], request.json['month'], request.json['year'])
        return json({
            'status': 'success',
            'data': data
        })
    except:
        return json({
            'status': 'false',
            'data': None
        })
    
    