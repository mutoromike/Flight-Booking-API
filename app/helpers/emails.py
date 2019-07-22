import os

from flask import render_template, jsonify, make_response
from flask_mail import Message, Mail
from app.models.models import User, Bookings, Flights

mail = Mail()


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
    try:
        mail.send(msg)
        return True
    except Exception as e:
        return False