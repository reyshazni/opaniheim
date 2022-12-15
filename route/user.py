from flask import Blueprint, request, session
from middleware.authentication import token_required
from services.otp_sender import create_session_from_otp
from controller.auth_controller import register_user_db, login_user_db
group = "user"
blueprint = Blueprint(group, __name__)

@blueprint.get(f"/otp/<otp_id>")
def create_session_with_otp(otp_id):
    return create_session_from_otp(otp_id)

@blueprint.post(f"/login")
def sign_in_user():
    data = request.get_json()
    return login_user_db(data["username"], data["password"])


@blueprint.post(f"/register")
def sign_up_user():
    data = request.get_json()
    try:
        return register_user_db(data["username"], data["password"], data["email"])
    except:
        return {
            "msg": "System fails"
        }, 500

