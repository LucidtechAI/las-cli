import contextlib
import collections
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


@contextlib.contextmanager
def wrap_output(start_msg: str, end_msg: str, error_msg: str=None):
    try:
        print(start_msg, end=' ')
        yield
    except:
        raise
        if error_msg:
            print(error_msg)
    finally:
        print(end_msg)
    

def capture_return(dest: list):
    def inner(f):
        @contextlib.wraps(f)
        def wrapper(*args, **kwargs):
            nonlocal dest 

            val = f(*args, **kwargs)
            dest += val if isinstance(val, collections.abc.Iterable) else [val]
            return val
    
        return wrapper

    return inner


