import json
from pathlib import Path


class NotProvided:
    pass


def nullable(value):
    if isinstance(value, str) and value == 'null':
        return None
    return value


def json_path(path):
    return json.loads(Path(path).read_text()) if path else None
