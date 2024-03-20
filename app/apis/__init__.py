from sanic import Blueprint

from app.apis.user_blueprint import user_blueprint
from app.apis.bill_blueprint import bill_blueprint
from app.apis.comment_blueprint import comment_blueprint
from app.apis.assets_blueprint import assets_blueprint
from app.apis.transactions_blueprint import transactions_blueprint
from app.apis.goals_blueprint import goals_blueprint

api = Blueprint.group([user_blueprint, bill_blueprint, comment_blueprint, assets_blueprint, transactions_blueprint, goals_blueprint])