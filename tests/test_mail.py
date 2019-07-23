from flask_mail import Mail, Message, BadHeaderError, sanitize_address, PY3
import json
from email.header import Header

from tests.base import BaseTestCase
class TestMessage(BaseTestCase):

    def test_initialize(self):
        msg = Message(subject="subject",
                      recipients=["to@example.com"])
        self.assertEqual(msg.sender, self.app.extensions['mail'].default_sender)
        self.assertEqual(msg.recipients, ["to@example.com"])

    def test_recipients_properly_initialized(self):
        msg = Message(subject="subject")
        self.assertEqual(msg.recipients, [])
        msg2 = Message(subject="subject")
        msg2.add_recipient("somebody@here.com")
        self.assertEqual(len(msg2.recipients), 1)

    def test_esmtp_options_properly_initialized(self):
        msg = Message(subject="subject")
        self.assertEqual(msg.mail_options, [])
        self.assertEqual(msg.rcpt_options, [])

        msg = Message(subject="subject", mail_options=['BODY=8BITMIME'])
        self.assertEqual(msg.mail_options, ['BODY=8BITMIME'])

        msg2 = Message(subject="subject", rcpt_options=['NOTIFY=SUCCESS'])
        self.assertEqual(msg2.rcpt_options, ['NOTIFY=SUCCESS'])

    def test_sendto_properly_set(self):
        msg = Message(subject="subject", recipients=["somebody@here.com"],
                      cc=["cc@example.com"], bcc=["bcc@example.com"])
        self.assertEqual(len(msg.send_to), 3)
        msg.add_recipient("cc@example.com")
        self.assertEqual(len(msg.send_to), 3)

    def test_add_recipient(self):
        msg = Message("testing")
        msg.add_recipient("to@example.com")
        self.assertEqual(msg.recipients, ["to@example.com"])

    def test_sender_as_tuple(self):
        msg = Message(subject="testing",
                      sender=("tester", "tester@example.com"))
        self.assertEqual('tester <tester@example.com>', msg.sender)

    def test_default_sender_as_tuple(self):
        self.app.extensions['mail'].default_sender = ('tester', 'tester@example.com')
        msg = Message(subject="testing")
        self.assertEqual('tester <tester@example.com>', msg.sender)

    def test_reply_to(self):
        msg = Message(subject="testing",
                      recipients=["to@example.com"],
                      sender="spammer <spammer@example.com>",
                      reply_to="somebody <somebody@example.com>",
                      body="testing")
        response = msg.as_string()

        h = Header("Reply-To: %s" % sanitize_address('somebody <somebody@example.com>'))
        self.assertIn(h.encode(), str(response))

    def test_send_without_recipients(self):
        msg = Message(subject="testing",
                      recipients=[],
                      body="testing")
        self.assertRaises(AssertionError, self.mail.send, msg)

    def test_bad_header_subject(self):
        msg = Message(subject="testing\r\n",
                      sender="from@example.com",
                      body="testing",
                      recipients=["to@example.com"])
        self.assertRaises(BadHeaderError, self.mail.send, msg)

    def test_plain_message(self):
        plain_text = "Hello Joe,\nHow are you?"
        msg = Message(sender="from@example.com",
                      subject="subject",
                      recipients=["to@example.com"],
                      body=plain_text)
        self.assertEqual(plain_text, msg.body)
        self.assertIn('Content-Type: text/plain', msg.as_string())

    def test_html_message(self):
        html_text = "<p>Hello World</p>"
        msg = Message(sender="from@example.com",
                      subject="subject",
                      recipients=["to@example.com"],
                      html=html_text)

        self.assertEqual(html_text, msg.html)
        self.assertIn('Content-Type: multipart/alternative', msg.as_string())

    def test_empty_subject_header(self):
        msg = Message(sender="from@example.com",
                      recipients=["foo@bar.com"])
        msg.body = "normal ascii text"
        self.mail.send(msg)
        self.assertNotIn('Subject:', msg.as_string())