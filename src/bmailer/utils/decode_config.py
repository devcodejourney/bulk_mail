import base64


def _decode(config: str) -> str:
    return base64.b64encode(config.encode()).decode()
