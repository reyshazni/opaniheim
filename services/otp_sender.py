import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import jwt
from middleware.authentication import encode_jwt

secret_key = "Opaniezzz"
jwt_algo = "HS256"

def otp_encoder(uid: int):
    payload = {
        "user_id": uid,
        "expires": time.time() + 9999999
    }
    token = jwt.encode(payload, secret_key, algorithm=jwt_algo)
    return token

def decode_otp(token: str):
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=[jwt_algo])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {
            "msg": "otp cannot be decoded"
        }, 503

def create_session_from_otp(otp: str):
    decoded = decode_otp(otp)
    token = encode_jwt(decoded["user_id"])
    try :
        return {
            "msg": "Session Created",
            "token": token
        }
    except:
        return {
            "msg": "Internal Server Error"
        }, 500

def send_otp(to_email: str, uid: int):
    msg = MIMEMultipart()
    fromaddr = "academic_stei@itb.ac.id"
    msg['Subject'] = "Verifikasi OTP"
    msg['From'] = fromaddr
    msg['To'] = to_email
    content = f"Kode OTP Anda adalah {otp_encoder(uid)} \n masukan ke /otp/[kode otp anda]"
    msg.attach(MIMEText(content, 'plain'))
    six_uname = "18220078"
    six_pwd = "mhsITB2020666764"
    print("start sending to", to_email)
    server = smtplib.SMTP("167.205.23.26", 587)
    server.starttls()
    server.login(six_uname, six_pwd)
    text = msg.as_string()
    server.sendmail(fromaddr, to_email, text)
    print("end..")
    server.quit()