from dataclasses import dataclass


@dataclass
class TrackingLink:
    url: str
    text: str = "URL here"
