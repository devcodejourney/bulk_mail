import logging
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def validate_email(email: str) -> bool:
    """Validate email with comprehensive regex"""
    pattern = r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None
