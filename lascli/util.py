import argparse
import collections
import contextlib
import json
from pathlib import Path


class NotProvided:
    pass


def nullable(_type=str):
    def _nullable(value):
        if isinstance(value, str) and value == 'null':
            return None
        return _type(value)
    return _nullable


def json_path(path):
    return json.loads(Path(path).read_text()) if path else None


@contextlib.contextmanager
def wrap_output(start_msg: str, end_msg: str, error_msg: str=None):
    try:
        print(start_msg, end=' ')
        yield
    except:
        if error_msg:
            print(error_msg)

        raise
    finally:
        print(end_msg)


def capture_return(dest: list):
    def inner(f):
        @contextlib.wraps(f)
        def wrapper(*args, **kwargs):
            nonlocal dest

            val = f(*args, **kwargs)
            dest += val if isinstance(val, (list, tuple)) else [val]
            return val

        return wrapper

    return inner


def json_or_json_path(value):
    if not value:
        return

    try:
        return json.loads(value)
    except json.JSONDecodeError:
        pass

    try:
        return json.loads(Path(value).read_text())
    except (json.JSONDecodeError, FileNotFoundError):
        pass

    raise Exception('Could not interpret input as neither JSON nor a path containing JSON')


def int_range(min_value, max_value):
    def checker(arg):
        try:
            value = int(arg)
        except ValueError:
            raise argparse.ArgumentTypeError('must be an integer')
        if not (min_value <= value <= max_value):
            raise argparse.ArgumentTypeError(f'must be in range [{min_value}..{max_value}]')
        return value

    return checker
