from flask_mail import Message, Mail
import random
from flask import jsonify, session, flash
from app.route.auth import Password_reset

app = Flask(__name__)
app.config['MAIL_SERVER'] = smtp.gmail.com
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'Wiriama'
app.config['MAIL_PASSWORD'] = 'ma98wi76'
app.config['MAIL_DEFAULT_SENDER'] = 'nicholasmawira6@gmail.com'
app.config['SECRET_KEY'] = 'Wiriama'

mail = Mail(app)
def gen_otp():
    return str(random.randint(00000, 99999))

def send_otp(email):
    otp = gen_otp()

    session[otp] = otp
    msg = Message("Your One-Time-Password", recipient=[email])
    mgs.body = f"Your one-time password is: {otp} valid for 10 minutes"

    try:
        mail.send(msg)
        flash(f"OTP send to {email}", "success")
     except Exception as e:
        flash(f"Error {e} ocurred when sending the mail")

    return otp
