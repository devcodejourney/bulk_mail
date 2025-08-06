from dataclasses import dataclass


@dataclass
class Recipient:
    email: str
    name: str = "No name"
