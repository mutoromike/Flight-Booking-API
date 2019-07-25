import os
from threading import Thread

from flask import render_template
from flask_mail import Message, Mail


mail = Mail()

def send_async_email(msg):
    from manage import app
    with app.app_context():
        mail.send(msg)


def send_approve(uname, email, name, origin, destination, date, time, seats):
    # send the email
    sender = os.getenv('MAIL_USERNAME')
    msg = Message('Your Reservation Has Been Approved',
                  recipients=[email], sender=sender)
    msg.html = render_template('send_email.html',
        uname=uname,
        email=email,
        name=name,
        origin=origin,
        destination=destination,
        date=date,
        time=time,
        seats=seats)
    thread = Thread(target=send_async_email, args=[msg])
    thread.start()
