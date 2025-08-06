import os
from dotenv import load_dotenv

load_dotenv()


class AppConfig:
    MAX_THREADS = int(os.getenv("MAX_THREADS", 10))
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", 100))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


class EmailConfig:
    SENDER_NAME = os.getenv("SENDER_NAME", "your_name")
    SENDER_EMAIL = os.getenv("SENDER_EMAIL", "your_email")
    REPLY_TO = os.getenv("REPLY_TO", "your_email")


class SmtpConfig:
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")  # default to Gmail
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "your_email")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your_password")


class ClientConfig:
    TIMEOUT = int(os.getenv("TIMEOUT", 30))
    RETRIES = int(os.getenv("RETRIES", 3))
    DELAY = int(os.getenv("DELAY", 2))
    CHARSET = "utf-8"


class TrackingConfig:
    TRACK_OPENS = True
    TRACK_CLICKS = True
    TRACKING_DOMAIN = os.getenv("TRACKING_DOMAIN", "track.yourdomain.com")
