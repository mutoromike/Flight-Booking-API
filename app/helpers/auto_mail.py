import os
import atexit
import logging
from datetime import datetime, timedelta

from flask import jsonify, make_response
from flask_mail import Message, Mail
from app.models.models import Bookings, User, Flights
import os

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

mail = Mail()


def get_bookings():
    date = str((datetime.now() + timedelta(days=1)).date())
    bookings = Bookings.query.filter(Bookings.booking_date==date).all()
    if not bookings:
        return False
    else:
        return bookings


def generate_message():
    bookings = get_bookings()
    if not bookings:
        return False
    message_list = []
    for booking in bookings:
        if booking.flight_status == "approved":
            user = User.query.filter_by(id=booking.client_id).first()
            flight = Flights.query.filter_by(id=booking.flight_id).first()
            msg = Message('Flight Reservation Reminder!',
                recipients=[user.email], sender="support@smartflights.com")
            msg.html = f'Hello {user.username},'
            f'<p> This is to remind you of your scheduled flight <b>{flight.name}</b>'
            f'from <b>{flight.origin}</b> on <b>{booking.booking_date}</b> </p>'
            f'<p> Please check in for your flight three hours before <b>{flight.time}</b>,'
            f' the DEPARTURE TIME</p>'
            f'<p> Thank you </p>'
            message_list.append(msg)
        else:
            pass
    return message_list


def send_email():
    print("we are here.......")
    from manage import app
    with app.app_context():
        bookings = get_bookings()
        if not bookings:
            logging.info("There are no RESERVATIONS FOR TOMORROW")
        else:
            logging.info("creating the mailing lists ...")
            messages = generate_message()

            logging.info("connecting to the mail server ...")
            for message in messages:
                try:
                    with app.app_context():
                        mail.send(message)
                        logging.info("sending success: " + str(message.recipients))
                except Exception as e:
                    logging.warning("sending failed: " + str(message.recipients))


def background_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=send_email,
        trigger=IntervalTrigger(start_date='2019-07-24 13:44:00', minutes=1),
        id='job_to_remind_clients',
        name='BACKGROUND JOB SENDING EMAILS',
        replace_existing=True)
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    atexit.register(lambda: scheduler.shutdown())