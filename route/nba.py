from flask import Blueprint, request

from controller.player_controller import get_player_information_normal, get_player_information_by_name, \
    delete_player_info
from middleware.authentication import token_required

group = "nba"
blueprint = Blueprint(group, __name__)

@token_required
@blueprint.delete(f"/{group}/player")
def delete_player():
    return delete_player_info(2)

@blueprint.post(f"/{group}/player")
def add_player(): pass

@blueprint.put(f"/{group}/player")
def update_player():
    return {
        "msf":"get"
    }

@blueprint.get(f"/{group}/player")
# @token_required
def get_player_info():
    limit = request.args.get('limit')
    if limit is None: limit = 10
    page = request.args.get('page')
    if page is None: page = 1
    player_name = request.args.get('name')
    if (player_name is not None):
        return get_player_information_by_name(limit=limit, page=page, player_name=player_name)
    return get_player_information_normal(limit=limit, page=page)