import argparse
import logging
import time
from pathlib import Path

from bmailer.modules.email import build_email
from bmailer.modules.sender import EmailSender
from bmailer.utils.validator import load_recipients
from config import EMAIL_CONFIG, TRACKING_CONFIG
from utils.logging_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
TEMPLATES_DIR = ROOT_DIR / "templates"


def main():
    parser = argparse.ArgumentParser(description="Bulk Email Sender Tool")
    parser.add_argument(
        "--recipients",
        default=DATA_DIR / "recipients.csv",
        help="Path to recipients CSV file",
    )
    parser.add_argument("--template", help="Email template to use (without extension)")
    parser.add_argument("--subject", required=True, help="Email subject")
    parser.add_argument(
        "--dry-run", action="store_true", help="Test without actually sending"
    )
    parser.add_argument(
        "--delay", type=float, default=1.0, help="Delay between emails in seconds"
    )

    args = parser.parse_args()

    try:
        # Load and validate recipients
        recipients = load_recipients(args.recipients)
        if not recipients:
            logger.error("No valid recipients found")
            return

        logger.info(f"Loaded {len(recipients)} valid recipients")

        # Initialize email sender
        sender = EmailSender(
            smtp_server=EMAIL_CONFIG["mta_server"],
            smtp_port=EMAIL_CONFIG["mta_port"],
            smtp_username=EMAIL_CONFIG["smtp_username"],
            smtp_password=EMAIL_CONFIG["smtp_password"],
            sender_email=EMAIL_CONFIG["sender_email"],
            retries=EMAIL_CONFIG["retries"],
            timeout=EMAIL_CONFIG["timeout"],
            delay=EMAIL_CONFIG["delay"],
        )
        success_count = 0
        fail_count = 0

        # Send emails
        for recipient in recipients:
            email_content = build_email(
                template_path=TEMPLATES_DIR,
                recipient_path=DATA_DIR / "recipients.csv",
                recipient_email=recipient["email"],
                sender_email=EMAIL_CONFIG["sender_email"],
                subject=args.subject,
                link_path=DATA_DIR / "links.csv",
                is_tracking_enabled=TRACKING_CONFIG["track_clicks"],
                tracking_domain=TRACKING_CONFIG["tracking_domain"],
                template_name=args.template,
            )

            if args.dry_run:
                logger.info(f"DRY RUN: Would send to {recipient['email']}")
                success_count += 1
            else:
                if sender.send(email_content):
                    success_count += 1
                else:
                    fail_count += 1

                time.sleep(args.delay)  # Throttle sending

        logger.info(f"Campaign complete: {success_count} sent, {fail_count} failed")

    except KeyboardInterrupt:
        logger.warning("Operation cancelled by user")

    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")


if __name__ == "__main__":
    main()
