from middleware.authentication import encode_jwt
from services.database_Service import conn as db_conn
from sqlalchemy import text
import re
import threading

from services.otp_sender import send_otp

def is_email(email: str):
    regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(regex, email)


def login_user_db(username: str, password: str):
    query = text("SELECT uid, email FROM users WHERE username=:username AND password=:password LIMIT 1")
    try:
        for user in db_conn.execute(query, {"username": username, "password": password}):
            thread = threading.Thread(target=send_otp, args=(user["email"],user["uid"],))
            thread.daemon = True
            thread.start()
            return {
                "msg": "Success, silahkan lihat email anda dan pergi ke /otp/[kode otp anda] ",
            }
        return {
                   "msg": "User not found"
               }, 404
    except:
        return  {
            "msg" : "Internal Server Error"
        }, 500

def register_user_db(username: str, password: str, email: str):
    if not is_email(email) : return {
        "msg" : "Not a valid email"
    }, 405
    query = text("INSERT INTO users(username, password, email) VALUES (:username, :password, :email)")
    try:
        result = db_conn.execute(query, {"username": username, "password": password, "email": email})
        if result.rowcount > 0:
            return {
                       "msg": "success"
                   }, 200
        return {
                   "msg": "System Fails"
               }, 500
    except:
        return {
            "msg": "fails, username is not unique"
        }, 502
