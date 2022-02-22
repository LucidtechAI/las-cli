from itertools import product
from pathlib import Path
from lascli.util import NotProvided


def main_parser(parser, client, argument_list):
    args = vars(parser.parse_args(argument_list))
    cmd = args.pop('cmd')
    _ = args.pop('profile', None)
    _ = args.pop('verbose')
    args['las_client'] = client
    kwargs = {k: v for k, v in args.items() if v != NotProvided}
    return cmd(**kwargs)


def assets_folder():
    return Path(__file__).parent / 'assets'


def max_results_and_next_token():
    max_results = [
        ('--max-results', '5'),
        (),
    ]
    next_token = [
        ('--next-token', 'foo'),
        (),
    ]
    return [ m + n for m in max_results for n in  next_token]
