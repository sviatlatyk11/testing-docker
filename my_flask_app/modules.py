from pymongo import MongoClient
from datetime import datetime
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
MONGODB_CONNECTION_STRING = os.getenv('MONGODB_CONNECTION_STRING')
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')

connection = MongoClient(MONGODB_CONNECTION_STRING)
database = connection.get_database("Portfolio")
collection = database.get_collection("Users")

class Email:
    @staticmethod
    def send_email(toaddr):
        # Email details
        fromaddr = "noreply@gmail.com"  # Displayed as sender (must be verified alias)
        subject = "Thank you for your interest!"
        body = "This is just a test email. Do not reply to this. Sviat is testing"

        # Creating the email message
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(GMAIL_USER, toaddr, text)
        except Exception as e:
            print(f"Failed to send email: {e}")
        finally:
            server.quit()

class Telegram:
    @staticmethod
    def send_message(message):
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        response = requests.post(url, data=payload)
        return response

class Database:
    @staticmethod
    def add_to_database(content):
        # Extract data from request
        name = content['name']
        email = content['email']
        phone_number = content['phone_number']
        time = datetime.now()

        # Insert data into MongoDB
        result = collection.insert_one({
            "name": name,
            "email": email,
            "phone_number": phone_number,
            "time": time
        })

        # Construct the message for Telegram
        message = (
            f"New registration:\n"
            f"----------------\n"
            f"Name: {name}\n"
            f"----------------\n"
            f"Email: {email}\n"
            f"----------------\n"
            f"Phone Number: {phone_number}\n"
            f"----------------\n"
            f"Time: {time}"
        )

        return result, message, email
