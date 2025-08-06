import csv
import random
import string

from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from typing import Dict, List, Optional

from config import EMAIL_CONFIG, TRACKING_CONFIG


def generate_message_id(sender_email: str) -> str:
    """Generate a unique message ID for email headers"""
    rand_part = "".join(random.choices(string.ascii_letters + string.digits, k=16))
    return f"<{rand_part}@{sender_email.split('@')[-1]}>"


def load_links(
    file_path: Path,
    is_tracking_enabled: bool = False,
    tracking_domain: Optional[str] = None,
) -> List:
    """Load links from CSV file"""
    links = []
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if is_tracking_enabled:
                row["url"] = f"http://{tracking_domain}/redirect?to={row['url']}"
            links.append(row)
    return links


def load_recipient_data(file_path: Path, email: str) -> Dict[str, str]:
    """Load additional recipient data from CSV"""
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["email"] == email:
                return row
    return {"email": email}


def build_email(
    template_path: Path,
    recipient_path: Path,
    recipient_email: str,
    sender_email: str,
    subject: str,
    link_path: Path,
    is_tracking_enabled: bool,
    tracking_domain: Optional[str] = None,
    template_name: Optional[str] = None,
):
    """Build complete email with headers and body"""
    # Load recipient data
    recipient_data = load_recipient_data(recipient_path, recipient_email)

    # Load templates
    env = Environment(loader=FileSystemLoader(template_path))
    html_template = env.get_template(
        template_name + ".html" if template_name else "default.html"
    )
    text_template = env.get_template(
        template_name + ".txt" if template_name else "default.txt"
    )

    # Generate tracking data
    message_id = generate_message_id(sender_email)
    links = load_links(link_path, is_tracking_enabled, tracking_domain)

    # Common template context
    context = {
        "recipient_email": recipient_email,
        "recipient_name": recipient_data.get("name", ""),
        "subject": subject,
        "links": links,
        "sender_name": EMAIL_CONFIG["sender_name"],
        "sender_email": EMAIL_CONFIG["sender_email"],
        "message_id": message_id,
        "tracking": TRACKING_CONFIG,
        "config": EMAIL_CONFIG,
    }

    # Render templates
    html_content = html_template.render(**context)
    text_content = text_template.render(**context)

    # Build email headers
    date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")

    email_data = f"""From: {EMAIL_CONFIG['sender_name']} <{EMAIL_CONFIG['sender_email']}>
To: {recipient_email}
Reply-To: {EMAIL_CONFIG['reply_to']}
Subject: {subject}
Date: {date}
Message-ID: {message_id}
MIME-Version: 1.0
Content-Type: multipart/alternative; boundary="BOUNDARY"

--BOUNDARY
Content-Type: text/plain; charset={EMAIL_CONFIG['charset']}

{text_content}

--BOUNDARY
Content-Type: text/html; charset={EMAIL_CONFIG['charset']}

{html_content}

--BOUNDARY--
"""
    return {"to": recipient_email, "data": email_data}
