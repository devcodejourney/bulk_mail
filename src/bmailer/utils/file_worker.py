import csv
import logging
from pathlib import Path
from typing import List, Optional

from bmailer.models.recipient import Recipient
from bmailer.models.tracking_link import TrackingLink
from bmailer.utils.validator import validate_email

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def load_links(
    file_path: Path,
    is_tracking_enabled: bool = False,
    tracking_domain: Optional[str] = None,
) -> List[TrackingLink]:
    """Load links from CSV file"""
    links: List[TrackingLink] = []
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if is_tracking_enabled:
                row["url"] = f"http://{tracking_domain}/redirect?to={row['url']}"
            link = TrackingLink(url=row["url"], text=row.get("text", ""))
            links.append(link)
    return links


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
