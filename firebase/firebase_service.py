import os
import firebase_admin
from firebase_admin import credentials, messaging
from dotenv import load_dotenv

load_dotenv()

cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")

if not cred_path:
    raise RuntimeError("❌ FIREBASE_CREDENTIALS_PATH not set")

cred = credentials.Certificate(cred_path)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)


def send_topic_notification(title: str, body: str, topic="energy_updates"):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        topic=topic
    )
    messaging.send(message)
