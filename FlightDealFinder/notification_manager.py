import os
from twilio.rest import Client

class NotificationManager:

    def __init__(self):
        self.client = Client(os.environ.get['TWILIO_SID'], os.environ.get["TWILIO_AUTH_TOKEN"])

    def send_sms(self, message_body):
        message = self.client.messages.create(
            from_=os.environ.get["TWILIO_VIRTUAL_NUMBER"],
            body=message_body,
            to=os.environ.get["YOUR_PHONE_NUMBER"]
        )
        print(message.sid)
