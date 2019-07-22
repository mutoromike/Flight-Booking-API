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
    print("the recipient is", email)
    msg.body = "Hello " + uname
    msg.html = render_template('templates/ticket.html',
        uname=uname,
        email=email,
        name=name,
        origin=origin,
        destination=destination,
        date=date,
        time=time,
        seats=seats)
    # print("we are here")
    # mail.send(msg)
    try:
        print("we sre here")
        mail.send(msg)
        # print("we sre here")
        response = {"message": "Email sent successfully"}
        return ake_response(jsonify(response))
    except Exception as e:
        return False
