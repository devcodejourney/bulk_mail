import os
import csv
from jinja2 import Environment, FileSystemLoader
from config import EMAIL_CONFIG, TRACKING_CONFIG
import random
import string
from datetime import datetime

def generate_message_id():
    """Generate a unique message ID for email headers"""
    rand_part = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    return f"<{rand_part}@{EMAIL_CONFIG['sender_email'].split('@')[-1]}>"

def load_links():
    """Load links from CSV file"""
    links = []
    with open('data/links.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if TRACKING_CONFIG['track_clicks']:
                row['url'] = f"http://{TRACKING_CONFIG['tracking_domain']}/redirect?to={row['url']}"
            links.append(row)
    return links

def load_recipient_data(email):
    """Load additional recipient data from CSV"""
    with open('data/recipients.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['email'] == email:
                return row
    return {'email': email}

def build_email(recipient_email, subject, template_name=None):
    """Build complete email with headers and body"""
    # Load recipient data
    recipient_data = load_recipient_data(recipient_email)
    
    # Load templates
    env = Environment(loader=FileSystemLoader('templates'))
    html_template = env.get_template(template_name + '.html' if template_name else 'default.html')
    text_template = env.get_template(template_name + '.txt' if template_name else 'default.txt')
    
    # Generate tracking data
    message_id = generate_message_id()
    links = load_links()
    
    # Common template context
    context = {
        'recipient_email': recipient_email,
        'recipient_name': recipient_data.get('name', ''),
        'subject': subject,
        'links': links,
        'sender_name': EMAIL_CONFIG['sender_name'],
        'sender_email': EMAIL_CONFIG['sender_email'],
        'message_id': message_id,
        'tracking': TRACKING_CONFIG,
        'config': EMAIL_CONFIG
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
    return {
        'to': recipient_email,
        'data': email_data
    }