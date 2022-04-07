from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Post, User, Internet
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.sql.functions import random, user
import smtplib
import platform

auth = Blueprint('auth', __name__)

os = platform.system()

@auth.route('/login', methods=['GET', 'POST'])
def login():
    password = "brokerAdmin!888"
    email ="admin@gmail.com"
    user = User.query.filter_by(email=email).first()

    if not user:
        new_user = User(email=email, contact="001", first_name="Broker", last_name="Admin", password=generate_password_hash(
                    password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        datetime_login = request.form.get('datetime_login')

        user = User.query.filter_by(email=email).first()
        admin = "admin@gmail.com"
        passwordAdmin = "brokerAdmin!888"

        if user:
            if email == admin:
                if check_password_hash(user.password, password):
                    flash('Welcome Admin..', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.admin_dashboard'))
                else:
                    flash('Incorrect password, try again.', category='error')
            elif check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                get_info_login = Internet(os=os,datetime_login=datetime_login,user_id=user.id)
                db.session.add(get_info_login)
                db.session.commit()
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    
    return render_template("login.html", user=current_user, logo=True)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot():
    return render_template("forgot_password.html",user=current_user, logo=True)


@auth.route('/send_to_email', methods=['GET','POST'])
def send():
    if request.method == 'POST':
        email = request.form.get('email')
        users = User.query.filter_by(email=email).first()
        my_id = 0

        if users:
            for owner in User.query.all():
                if owner.email == email:
                    my_id=owner.id

            flash('Please check your email address.', category='success')
            # For HTML sending emails
            import smtplib

            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText

            # me == my email address
            # you == recipient's email address
            me = "BROKER"
            you = email

            # Create message container - the correct MIME type is multipart/alternative.
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "BROKER - Set New Password"
            msg['From'] = me
            msg['To'] = you

            # Create the body of the message (a plain-text and an HTML version).
            text = "Hi!\nWelcome to Broker Zamboanga - House and Lot Price Prediction\nHere is the link for you to access:\n http://127.0.0.1:5000/"
            html = f"""\
            <html>
                <head>
                </head>
            <body>
                <div style="background: #0f3142;height: 10vh;width: 100%;display: flex;justify-content: center;align-items: center"></div>
                <p>Hi!<br>
                Welcome to Broker Zamboanga - House and Lot Price Prediction<br>
                Here is the <a href="http://127.0.0.1:5000/set_new_pass/{my_id}">link</a> for your requested reset password.
                </p>
            </body>
            </html>
            """

            # Record the MIME types of both parts - text/plain and text/html.
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')

            # Attach parts into message container.
            # According to RFC 2046, the last part of a multipart message, in this case
            # the HTML message, is best and preferred.
            msg.attach(part1)
            msg.attach(part2)

            # Send the message 
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login("brokerzamboanga@gmail.com","longSpan#12")
            server.send_message(msg)
            server.quit()

        else:
            flash('Unable to get the request. Email address was not found', category='error')

    return render_template("forgot_password.html",user=current_user, logo=True)

#send the id to the reset form
@auth.route('/set_new_pass/<int:id>', methods=['GET','POST'])
def set_new_pass(id):
    return render_template("set_new_pass.html", my_id=id, user=current_user, logo=True)

# submit the new password to the database
@auth.route('/submit_new_pass/<int:id>', methods=['GET','POST'])
def save_new_pass(id):
    user = User.query.get_or_404(id)
    owner = User.query.filter_by(id=id).first()

    if request.method == "POST":
        id=request.form['my_id']
        password1=request.form['password1']
        password2=request.form['password2']

        if password1 != password2:
            flash('Passwords don\'t match.', category='error')
        else:
            if owner:
                user.password = generate_password_hash(password1, method='sha256')

            db.session.commit()
            flash("New password successfully update..")
            return redirect('/forgot_password')
            

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        contact = request.form.get('contact_no')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        datetime_login = request.form.get('datetime_login')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(contact) < 5:
            flash('Contact number is too short.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # For HTML sending emails
            import smtplib

            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText

            # me == my email address
            # you == recipient's email address
            me = "BROKER"
            you = email

            # Create message container - the correct MIME type is multipart/alternative.
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "BROKER"
            msg['From'] = me
            msg['To'] = you

            # Create the body of the message (a plain-text and an HTML version).
            text = "Hi!\nWelcome to Broker Zamboanga - House and Lot Price Prediction\nHere is the link for you to access:\n http://127.0.0.1:5000/"
            html = """\
            <html>
                <head>
                    <style>
                        .header {
                            background: #0f3142;
                            height: 10vh;
                            width: 100%;
                            display: flex;
                            justify-content: center;
                            align-items: center
                        }
                    </style>
                </head>
            <body>
                <div class="header"></div>
                <p>Hi!<br>
                Welcome to Broker Zamboanga - House and Lot Price Prediction<br>
                Here is the <a href="http://127.0.0.1:5000/">link</a> for you to access.
                </p>
            </body>
            </html>
            """

            # Record the MIME types of both parts - text/plain and text/html.
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')

            # Attach parts into message container.
            # According to RFC 2046, the last part of a multipart message, in this case
            # the HTML message, is best and preferred.
            msg.attach(part1)
            msg.attach(part2)

            # Send the message 
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login("brokerzamboanga@gmail.com","longSpan#12")
            server.send_message(msg)
            server.quit()


            # add to db user and commit
            new_user = User(email=email, contact=contact, first_name=first_name, last_name=last_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            get_info_login = Internet(os=os,datetime_login=datetime_login,user_id=new_user.id)
            db.session.add(get_info_login)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("register.html", user=current_user, logo=True)
