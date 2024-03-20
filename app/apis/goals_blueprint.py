from sanic import Blueprint
from sanic.response import json
from app.databases.mongodb import MongoDB

goals_blueprint = Blueprint('goals', url_prefix='/goals')

_db = MongoDB()

@goals_blueprint.route('/', methods={'GET'})
async def base(request):
    return json({
        "message": "Goals"
    })
    
@goals_blueprint.route('/get', methods={'POST'})
async def get_user_transactions(request):
    try :
        data = _db.get_user_transactions(request.json['username'])
        return json({
            'status': 'success',
            'data': data
        })
    except:
        return json({
            'status': 'false',
        })
    

@goals_blueprint.route('/add', methods={'POST'})
async def add_goal(request):
    try :
        data = _db.add_goal(request.json['username'], request.json['day'], request.json['month'], request.json['year'], 
                                   request.json['name'], request.json['money'], request.json['time'], request.json['unit'],
                                   request.json['img'])
        return json({
            'status': 'success',
            'data': data
        })
    except:
        return json({
            'status': 'false',
            'data': None
        })
    
    
@goals_blueprint.route('/delete', methods={'POST'})
async def delete_goal(request):
    try :
        data = _db.delete_goal(request.json['username'], request.json['day'], request.json['month'], request.json['year'], 
                                   request.json['name'], request.json['money'], request.json['time'], request.json['unit'],
                                   request.json['img'])
        return json({
            'status': 'success',
            'data': data
        })
    except:
        return json({
            'status': 'false',
            'data': None
        })