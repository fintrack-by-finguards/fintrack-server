from sanic import Blueprint

from app.apis.blueprint import user_blueprint

api = Blueprint.group([user_blueprint])