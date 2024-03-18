from sanic import Blueprint
from sanic.response import json
from app.databases.mongodb import MongoDB

transactions_blueprint = Blueprint('transactions', url_prefix='/transactions')

_db = MongoDB()

@transactions_blueprint.route('/', methods={'GET'})
async def base(request):
    return json({
        "message": "Transactions"
    })
    
@transactions_blueprint.route('/get', methods={'POST'})
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
    

@transactions_blueprint.route('/getOne', methods={'POST'})
async def get_user_transactions_specific(request):
    try :
        data = _db.get_user_transactions_specific(request.json['username'], request.json['day'], request.json['month'], request.json['year'])
        return json({
            'status': 'success',
            'data': data
        })
    except:
        return json({
            'status': 'false',
            'data': None
        })
    

@transactions_blueprint.route('/add', methods={'POST'})
async def add_transaction(request):
    try :
        data = _db.add_transaction(request.json['username'], request.json['day'], request.json['month'], request.json['year'], 
                                   request.json['name'], request.json['category1'], request.json['category2'], request.json['money'],
                                   request.json['hour'], request.json['minute'], request.json['second'], request.json['type'],)
        return json({
            'status': 'success',
            'data': data
        })
    except:
        return json({
            'status': 'false',
            'data': None
        })
    
@transactions_blueprint.route('/update', methods={'POST'})
async def update_transaction(request):
    try :
        data = _db.update_transaction(request.json['username'], request.json['day'], request.json['month'], request.json['year'], 
                                   request.json['name'], request.json['category1'], request.json['category2'], request.json['money'],
                                   request.json['hour'], request.json['minute'], request.json['second'], request.json['type'],
                                   request.json['new_name'], request.json['new_category1'], request.json['new_category2'], request.json['new_money'],
                                   request.json['new_hour'], request.json['new_minute'], request.json['new_second'], request.json['new_type'])
        return json({
            'status': 'success',
            'data': data
        })
    except:
        return json({
            'status': 'false',
            'data': None
        })
    
@transactions_blueprint.route('/delete', methods={'POST'})
async def delete_transaction(request):
    try :
        data = _db.delete_transaction(request.json['username'], request.json['day'], request.json['month'], request.json['year'], 
                                   request.json['name'], request.json['category1'], request.json['category2'], request.json['money'],
                                   request.json['hour'], request.json['minute'], request.json['second'], request.json['type'])
        return json({
            'status': 'success',
            'data': data
        })
    except:
        return json({
            'status': 'false',
            'data': None
        })

@transactions_blueprint.route('/getMonthYear', methods={'POST'})
async def get_user_transactions_specific_month_year(request):
    try :
        data = _db.get_user_transactions_specific_month_year(request.json['username'], request.json['month'], request.json['year'])
        return json({
            'status': 'success',
            'data': data
        })
    except:
        return json({
            'status': 'false',
            'data': None
        })
    
    
    