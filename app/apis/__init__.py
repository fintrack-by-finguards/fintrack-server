from sanic import Blueprint

from app.apis.user_blueprint import user_blueprint
from app.apis.bill_blueprint import bill_blueprint

api = Blueprint.group([user_blueprint, bill_blueprint])