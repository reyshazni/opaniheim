from flask import Blueprint, request

from controller.player_controller import get_player_information_normal, get_player_information_by_name, \
    delete_player_info, update_player_name
from middleware.authentication import token_required

group = "nba"
blueprint = Blueprint(group, __name__)

@token_required
@blueprint.delete(f"/{group}/player")
def delete_player(token):
    data = request.get_json()
    try:
        player_rk = int(data["player_rk"])
        return delete_player_info(player_rk=player_rk)
    except:
        return {
            "msg": "Bad Request"
        }, 500

@blueprint.post(f"/{group}/player")
def add_player(): pass

@token_required
@blueprint.put(f"/{group}/player")
def update_player():
    data = request.get_json()
    try:
        player_rk = data["player_rk"]
        new_name = data["new_name"]
        return update_player_name(player_rk=player_rk, new_name=new_name)
    except:
        return {
                "msg": "Bad Request"
        }, 500

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