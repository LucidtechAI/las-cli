from pathlib import Path
import yaml


class NotProvided:
    pass


def nullable(value):
    if isinstance(value, str) and value == 'null':
        return None
    return value


def dictionary(value: str):
    """ Parse input as a .json or .yaml file if the file exists, if not parse input directly as a json string"""
    if not value:
        return None

    path = Path(value)

    if path.is_file():
        value = Path(value).read_text()
    elif path.suffix in ['.json', '.yaml', '.yml']:
        raise FileNotFoundError(f'Could not find {value}')

    try:
        return yaml.safe_load(value)
    except yaml.parser.ParserError:
        raise ValueError(
            f'{value} could not be parsed as a dictionary, make sure the string is valid json or yaml: {value}'
        )
