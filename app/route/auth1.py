""" authenticate user it has this funtions
: login
: signup
: reset_password"""

from flask import Blueprint, request, render_template, session, redirect, flash, url_for, jsonify
from flask_bcrypt import Bcrypt
from app.models.user import User
from app.extension import db

bcrypt = Bcrypt()
auth = Blueprint('auth', __name__)

# hash password
def hash_password(password):
    try:
        return bcrypt.generate_password_hash(password).decode('utf-8')
    except Exception as e:
        raise RuntimeError(f"Password hashing failed: {str(e)}")

class Auth:
    """ class auth """
    @auth.route('/login', methods=["POST", "GET"])
    def login():
        """ Authenticating user login """
        if session.get('user_id'):
            """ if user in session """
            return redirect(url_for('home'))

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter_by(username=username).first()

            if user and bcrypt.check_password_hash(user.hashed_password, password):
                flash("login successfully", "success")
                session['user_id'] = user.id
                return redirect(url_for('home'))
            else:
                flash("Wrong details", "danger")

        return render_template('Login.html')

    @auth.route('/signup', methods=["POST", "GET"])
    def signup():
        """ add new user to system """
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')

            user_by_username = User.query.filter_by(username=username).first()
            user_by_email = User.query.filter_by(email=email).first()
            if user_by_username:
                flash(f"Username {username} Exist", "danger")
                return redirect(url_for('auth.signup'))

            if user_by_email:
                flash(f"{email} Exist", "danger")
                return redirect(url_for('auth.signup'))
 
            hashed_password = hash_password(password)
            new_user = User(username=username, email=email, hashed_password=hashed_password)
            db.session.add(new_user)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                flash("An error occurred while creating your account. Please try again.", "danger")
                return redirect(url_for('auth.signup'))
            user = User.query_all()
            flash("Account created successfully. Please log in.", "success")
            print(f"{user}")
            return redirect(url_for('auth.login'))

        return render_template('register.html')

    @auth.route('/forgotten', methods=["POST", "GET"])
    def forgotten():
        """ resetting password if fogotten """
        if request.method == 'POST':
            email = request.form.get('email')

            user = User.query.filter_by(email=email).first()

            if not user:
                flash("Email Not Found", 'danger')
                return redirect(url_for('auth.password_reset'))

            send_otp = __import__(app.models.emailing).send_otp()
            session['otp'] = send_otp(email)
            session['email'] = email

            return redirect(url_for('auth.reset_password'))
        return render_template("pass_reset.html")

    @auth.route('reset_password', methods=["POST", "GET"])
    def reset_password():
        email_otp = session.get('otp')
        user_email = session.get('email')
        if request.method == 'POST':
            otp = request.form.get('otp')
            password = request.form.get('password')

            if not email_otp or not user_email:
                flash("Invalid or expired OTP")
                return redirect(url_for('auth.forgotten'))

            if otp == email_otp:
                flash("OTP verified", "success")
                user = User.query_by(email=user_email).first()

                if user:
                    user.hashed_password = hash_password(new_password)

                    db.session.add(user)
                    db.session.commit()

                    flash("Password reset success", "success")
                    return redirect(url_for('auth.login'))
                else:
                    flash("Invali OTP", "danger")
                    return redirect(url_for('auth.reset_password'))

        return render_template("reset.html")
