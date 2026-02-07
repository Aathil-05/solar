import os
import firebase_admin
from firebase_admin import credentials, messaging
from dotenv import load_dotenv
from fastapi import APIRouter

router = APIRouter(prefix="/notification", tags=["notification"])

load_dotenv()

cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")

if not cred_path:
    raise RuntimeError("❌ FIREBASE_CREDENTIALS_PATH not set")

cred = credentials.Certificate(cred_path)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)


def send_topic_notification(title: str, body: str, topic="energy_updates"):
    message = messaging.Message(
        data={
            "title": title,
            "body": body,
            "type": "energy"
        },
        topic=topic
    )
    messaging.send(message)


@router.post("/")
def send_demo_notification():
    send_topic_notification("Test", "Test notification")
    return {"status": "sent"}
