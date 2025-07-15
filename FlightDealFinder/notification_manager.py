import smtplib
import os
from twilio.rest import Client


class NotificationManager:
    """
    Handles sending SMS via Twilio and sending emails via SMTP
    using credentials and configuration from environment variables.
    """

    def __init__(self):
        # --- Load credentials and config from environment variables ---
        self.smtp_address = os.environ["EMAIL_PROVIDER_SMTP_ADDRESS"]
        self.email = os.environ["MY_EMAIL"]
        self.email_password = os.environ["MY_EMAIL_PASSWORD"]

        self.twilio_virtual_number = os.environ["TWILIO_VIRTUAL_NUMBER"]
        self.twilio_verified_number = os.environ["YOUR_PHONE_NUMBER"]

        # --- Initialize Twilio Client ---
        self.client = Client(
            os.environ["TWILIO_SID"],
            os.environ["TWILIO_AUTH_TOKEN"]
        )

    def send_sms(self, message_body):
        """
        Sends an SMS using Twilio's API.
        """
        message = self.client.messages.create(
            from_=self.twilio_virtual_number,
            body=message_body,
            to=self.twilio_verified_number
        )
        print(f"SMS sent with SID: {message.sid}")

    def send_emails(self, email_list, email_body):
        """
        Sends an email to each address in the provided list.
        Uses a secure SMTP connection with TLS.
        """
        with smtplib.SMTP(self.smtp_address) as connection:
            connection.starttls()  # Secure the connection
            connection.login(self.email, self.email_password)

            for recipient in email_list:
                connection.sendmail(
                    from_addr=self.email,
                    to_addrs=recipient,
                    msg=f"Subject: New Low Price Flight!\n\n{email_body}".encode("utf-8")
                )
                print(f"Email sent to {recipient}")
