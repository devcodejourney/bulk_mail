import csv
from pathlib import Path
from typing import List, Optional

from bmailer.models.tracking_link import TrackingLink


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
