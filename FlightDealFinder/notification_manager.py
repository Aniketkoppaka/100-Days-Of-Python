import os
from twilio.rest import Client

class NotificationManager:
    """
    Manages sending SMS notifications using the Twilio API.
    Requires the following environment variables to be set:
      - TWILIO_SID
      - TWILIO_AUTH_TOKEN
      - TWILIO_VIRTUAL_NUMBER (Twilio number used to send messages)
      - YOUR_PHONE_NUMBER (your verified recipient number)
    """

    def __init__(self):
        # Use os.environ.get() with () not [] — you had a syntax error
        # Initializes the Twilio client with credentials from environment variables
        self.client = Client(
            os.environ.get("TWILIO_SID"),
            os.environ.get("TWILIO_AUTH_TOKEN")
        )

    def send_sms(self, message_body):
        """
        Sends an SMS message with the specified body content.
        
        Parameters:
        - message_body (str): The content/text of the SMS to send.
        """
        # Creates and sends a new SMS message using Twilio
        message = self.client.messages.create(
            from_=os.environ.get("TWILIO_VIRTUAL_NUMBER"),  # Your Twilio number
            body=message_body,                              # Message content
            to=os.environ.get("YOUR_PHONE_NUMBER")          # Your recipient number
        )

        # Print the message SID (unique Twilio message identifier)
        print(f"[SMS Sent] Message SID: {message.sid}")
