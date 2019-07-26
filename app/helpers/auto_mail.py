import atexit
import logging
from datetime import datetime, timedelta

from flask import render_template
from flask_mail import Message, Mail
from app.models.models import Bookings, User, Flights

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

mail = Mail()


def get_bookings():
    date = str((datetime.now() + timedelta(days=1)).date())
    flights = Flights.query.filter(Flights.date==date).all()
    bookings = []
    for flight in flights:
        booking = Bookings.query.filter_by(flight_id=flight.id).first()
        bookings.append(booking)
    if not bookings:
        return False
    else:
        print("the bookings are", bookings)
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
            msg.html = render_template('reminder_mail.html',
                username=user.username,
                name=flight.name,
                origin=flight.origin,
                date=flight.date,
                time=flight.time
            )

            message_list.append(msg)
        else:
            pass
    return message_list


def send_email():
    from manage import app
    with app.app_context():
        bookings = get_bookings()
        if not bookings:
            logging.info("There are no RESERVATIONS FOR TOMORROW")
        else:
            logging.info("GENERATING EMAILS...")
            messages = generate_message()

            logging.info("CONNECTING MAIL SERVICE...")
            for message in messages:
                try:
                    with app.app_context():
                        mail.send(message)
                        logging.info("SENDING MAILS SUCCESSFUL " + str(message.recipients))
                except Exception as e:
                    logging.warning("SENDING MAILS SUCCESSFUL " + str(message.recipients))


def background_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=send_email,
        trigger=IntervalTrigger(start_date='2019-07-26 12:52:00', days=1),
        id='job_to_remind_clients',
        name='BACKGROUND JOB SENDING EMAILS',
        replace_existing=True)
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    atexit.register(lambda: scheduler.shutdown())