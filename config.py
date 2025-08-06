import os
from dotenv import load_dotenv

load_dotenv()

# Email configuration
EMAIL_CONFIG = {
    "sender_name": os.getenv("SENDER_NAME", "your_name"),
    "sender_email": os.getenv("SENDER_EMAIL", "your_email"),
    "reply_to": os.getenv("REPLY_TO", "your_email"),
    "mta_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),  # default to Gmail
    "mta_port": int(os.getenv("SMTP_PORT", "587")),
    "smtp_username": os.getenv("SMTP_USERNAME", "your_email"),
    "smtp_password": os.getenv("SMTP_PASSWORD", "your_password"),
    "timeout": int(os.getenv("TIMEOUT", "30")),
    "retries": int(os.getenv("RETRIES", "3")),
    "delay": int(os.getenv("DELAY", 2)),
    "charset": "utf-8",
}


# Tracking configuration
TRACKING_CONFIG = {
    "track_opens": True,  # Enables open tracking by embedding an invisible pixel in the email
    "track_clicks": True,  # Enables click tracking by rewriting links to go through a tracking server
    "tracking_domain": "track.yourdomain.com",  # The domain used to track link clicks (e.g. your own tracking server or service)
}

# Application settings
APP_CONFIG = {
    "max_threads": 10,  # Number of threads used for sending emails concurrently (for speed)
    "batch_size": 100,  # Number of emails to send in one batch
    "log_level": "INFO",  # Logging level: DEBUG (verbose), INFO (normal), WARNING, ERROR
}
