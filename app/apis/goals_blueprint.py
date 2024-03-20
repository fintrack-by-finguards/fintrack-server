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
async def get_goal(request):
    try :
        data = _db.get_goal(request.json['username'])
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
                                   request.json['img'], request.json['type'])
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
        data = _db.delete_goal(request.json['username'], request.json['id'])
        return json({
            'status': 'success',
            'data': data
        })
    except:
        return json({
            'status': 'false',
            'data': None
        })
    
@goals_blueprint.route('/update', methods={'POST'})
async def update_goal(request):
    try :
        data = _db.update_goal(request.json['username'], request.json['id'], request.json['day'], request.json['month'],
                               request.json['year'], request.json['name'], request.json['money'], request.json['time'],
                               request.json['unit'], request.json['img'], request.json['type'])
        return json({
            'status': 'success',
            'data': data
        })
    except:
        return json({
            'status': 'false',
            'data': None
        })
    
@goals_blueprint.route('/add_transaction', methods={'POST'})
async def add_goal_history(request):
    try :
        data = _db.add_goal_history(request.json['username'], request.json['id'], request.json['tran_id'], request.json['day'], 
                                   request.json['month'], request.json['year'], request.json['name'], request.json['money'],
                                   request.json['hour'], request.json['minute'], request.json['second'], request.json['moneytype'])
        return json({
            'status': 'success',
            'data': data
        })
    except:
        return json({
            'status': 'false',
            'data': None
        })

@goals_blueprint.route('/delete_transaction', methods={'POST'})
async def delete_goal_transaction(request):
    try :
        data = _db.delete_goal_transaction(request.json['username'], request.json['tran_id'])
        return json({
            'status': 'success',
            'data': data
        })
    except:
        return json({
            'status': 'false',
            'data': None
        })
