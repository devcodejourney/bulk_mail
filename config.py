# Email configuration
EMAIL_CONFIG = {
    'sender_name': 'Your Name',  # The name that will appear as the sender in the recipient's inbox
    'sender_email': 'you@example.com',  # The sender's email address (must match the SMTP credentials)
    'reply_to': 'reply@example.com',  # The email address where replies should be sent (can be different from sender_email)
    'mta_server': 'smtp.gmail.com',  # SMTP server address (e.g., Gmail SMTP server)
    'mta_port': 587,  # SMTP port number. Use 587 for STARTTLS (secure but not SSL)
    'smtp_username': 'you@example.com',  # The SMTP username (usually the same as sender_email)
    'smtp_password': 'your_app_password_here',  # The SMTP password or app password (never use your real email password)
    'timeout': 30,  # Timeout (in seconds) for connecting to the SMTP server
    'retries': 3,  # Number of times to retry sending email if it fails
    'delay': 2,  # Delay (in seconds) between retries if sending fails
    'charset': 'utf-8',  # Character encoding for the email content (UTF-8 supports all languages)
}



# Tracking configuration
TRACKING_CONFIG = {
    'track_opens': True,  # Enables open tracking by embedding an invisible pixel in the email
    'track_clicks': True,  # Enables click tracking by rewriting links to go through a tracking server
    'tracking_domain': 'track.yourdomain.com',  # The domain used to track link clicks (e.g. your own tracking server or service)
}

# Application settings
APP_CONFIG = {
    'max_threads': 10,  # Number of threads used for sending emails concurrently (for speed)
    'batch_size': 100,  # Number of emails to send in one batch
    'log_level': 'INFO',  # Logging level: DEBUG (verbose), INFO (normal), WARNING, ERROR
}