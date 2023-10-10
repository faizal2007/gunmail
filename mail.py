#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Read email account credentials from environment variables
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
SMTP_PORT = os.getenv('SMTP_PORT')

# Retrieve the "From" email address from the .env file
FROM_EMAIL = os.getenv('FROM_EMAIL')

# Retrieve the SMTP server hostname from the .env file
SMTP_HOSTNAME = os.getenv('SMTP_HOSTNAME')

# Retrieve the ENABLE_STARTTLS variable from the .env file (as a boolean)
ENABLE_STARTTLS = os.getenv('ENABLE_STARTTLS').lower() == 'true'

def send_email(subject, body, recipient_email):
    try:
        # Create a MIME object to represent the email
        msg = MIMEMultipart()
        msg["From"] = FROM_EMAIL
        msg["To"] = recipient_email
        msg["Subject"] = subject

        # Email body
        msg.attach(MIMEText(body, "plain"))

        # Connect to the SMTP server using the retrieved hostname
        server = smtplib.SMTP(SMTP_HOSTNAME, SMTP_PORT)
        
        if ENABLE_STARTTLS:
            server.starttls()
        
        server.login(SMTP_USERNAME, SMTP_PASSWORD)

        # Send the email
        text = msg.as_string()
        server.sendmail(FROM_EMAIL, recipient_email, text)

        # Close the SMTP connection
        server.quit()

        print(f"Email sent successfully to {recipient_email}")
    except smtplib.SMTPException as e:
        print(f"SMTP Error: {str(e)}")
    except Exception as e:
        print(f"Error sending email to {recipient_email}: {str(e)}")

# Read the list of recipients from "generated_email.txt" file
with open("files/generated_email.txt", "r") as file:
    recipient_emails = file.read().splitlines()

# Create and send emails to each recipient with progress indicator
total_recipients = len(recipient_emails)
for index, recipient_email in enumerate(recipient_emails, start=1):
    subject = "Hello from Python!"
    body = "This is a test email sent from Python with authentication."
    send_email(subject, body, recipient_email)

    # Display progress
    print(f"Progress: {index}/{total_recipients} emails sent")
