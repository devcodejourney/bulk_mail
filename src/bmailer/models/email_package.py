from dataclasses import dataclass


@dataclass
class EmailPackage:
    to: str
    data: str
