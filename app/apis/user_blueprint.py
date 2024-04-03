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
        res = _db.create_user(request.json['username'], request.json['password'], request.json['name'], request.json['birthday'],request.json['createday'], request.json['job'], request.json['university'])
        return res
    except:
        return json({
            'status': 'false',
        })
    
@user_blueprint.route('/update', methods={'POST'})
async def change_user_info(request):
    try :
        data = _db.change_user_info(request.json['username'], request.json['name'], request.json['birthday'],request.json['createday'], request.json['job'], request.json['university'], request.json['income'], request.json['activate'])
        return json({
            'status': 'success',
            'data': data
        })
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
    
@user_blueprint.route('/info', methods={'POST'})
async def get_info(request):
    try :
        data = _db.get_info()
        return json({
            'status': 'success',
            'data': data
        })
    except:
        return json({
            'status': 'false',
        })
    
    

