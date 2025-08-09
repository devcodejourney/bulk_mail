import csv
import logging
import re
from pathlib import Path
from typing import List

from bmailer.models.recipient import Recipient

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def validate_email(email: str) -> bool:
    """Validate email with comprehensive regex"""
    pattern = r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def load_recipients(file_path: Path) -> List[Recipient]:
    """Load and validate recipients from CSV"""
    valid_recipients = []

    try:
        with open(file_path, mode="r", encoding="utf-8") as f:
            dialect = csv.Sniffer().sniff(f.read(1024))
            f.seek(0)

            reader = csv.DictReader(f, dialect=dialect)

            if not reader.fieldnames:
                logger.error("CSV file is empty or has no headers")
                return []

            if "email" not in reader.fieldnames:
                logger.error("CSV must contain 'email' column")
                return []

            for row in reader:
                email = row["email"].strip()
                if validate_email(email):
                    name = row.get("name", "").strip()
                    valid_recipients.append(Recipient(email=email, name=name))
                else:
                    logger.warning(f"Invalid email skipped: {email}")

        logger.info(f"Loaded {len(valid_recipients)} valid recipients")
        return valid_recipients

    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return []

    except Exception as e:
        logger.error(f"Error reading CSV: {str(e)}")
        return []
