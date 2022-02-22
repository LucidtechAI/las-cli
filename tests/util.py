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


def metadata_path():
    return assets_folder() / 'metadata.json'


def preprocess_config_path():
    return assets_folder() / 'preprocess_config.json'


def field_config_path():
    return assets_folder() / 'field_config.json'


def schema_path():
    return assets_folder() / 'schema.json'


def error_config_path():
    return assets_folder() / 'workflow_error_config.json'


def transition_parameters_path():
    return assets_folder() / 'transition_parameters.json'


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


def ground_truth_options():
    return [
        ('--ground-truth-fields', 'foo=bar', 'baz=5'),
        ('--ground-truth-path', str(assets_folder() / 'gt.json')),
        ()
    ]


def name_and_description():
    name = [
        ('--name', 'foo'),
        ('--name', 'null'),
        (),
    ]
    description = [
        ('--description', 'bar baz'),
        ('--description', 'null'),
        (),
    ]
    return [ n + d for n in name for d in  description]
