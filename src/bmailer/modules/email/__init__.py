import csv
import random
import string

from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from typing import Dict, List, Optional

from bmailer.models.email_package import EmailPackage
from bmailer.models.tracking_link import TrackingLink


def generate_message_id(sender_email: str) -> str:
    """Generate a unique message ID for email headers"""
    rand_part = "".join(random.choices(string.ascii_letters + string.digits, k=16))
    return f"<{rand_part}@{sender_email.split('@')[-1]}>"


def load_recipient_data(file_path: Path, email: str) -> Dict[str, str]:
    """Load additional recipient data from CSV"""
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["email"] == email:
                return row
    return {"email": email}


# Hardcoded charset for email content
CHARSET = "utf-8"


def build_email(
    template_path: Path,
    recipient_email: str,
    recipient_name: str,
    sender_email: str,
    sender_name: str,
    reply_to: str,
    subject: str,
    track_opens: bool = False,
    tracking_domain: str = "",
    links: List[TrackingLink] = [],
    template_name: Optional[str] = None,
) -> EmailPackage:
    """Build complete email with headers and body"""
    # Load templates
    env = Environment(loader=FileSystemLoader(template_path))
    if template_name is None:
        template_name = "default"
    html_template = env.get_template(template_name + ".html")
    text_template = env.get_template(template_name + ".txt")

    # Generate tracking data
    message_id = generate_message_id(sender_email)

    # Common template context
    context = {
        "recipient_email": recipient_email,
        "recipient_name": recipient_name,
        "subject": subject,
        "links": links,
        "sender_name": sender_name,
        "sender_email": sender_email,
        "message_id": message_id,
        "track_opens": track_opens,
        "tracking_domain": tracking_domain,
        "charset": CHARSET,
    }

    # Render templates
    html_content = html_template.render(**context)
    text_content = text_template.render(**context)

    # Build email headers
    date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")

    email_data = f"""From: {sender_name} <{sender_email}>
To: {recipient_email}
Reply-To: {reply_to}
Subject: {subject}
Date: {date}
Message-ID: {message_id}
MIME-Version: 1.0
Content-Type: multipart/alternative; boundary="BOUNDARY"

--BOUNDARY
Content-Type: text/plain; charset={CHARSET}

{text_content}

--BOUNDARY
Content-Type: text/html; charset={CHARSET}

{html_content}

--BOUNDARY--
"""
    return EmailPackage(to=recipient_email, data=email_data)
