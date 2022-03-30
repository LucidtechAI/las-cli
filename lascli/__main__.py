#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import argparse
import configparser
import json
import logging
import textwrap

import argcomplete

from las import Client, Credentials
from las.credentials import MissingCredentials, read_from_file

from .__version__ import __version__
from .util import NotProvided
from .parser import (
    create_app_clients_parser,
    create_assets_parser,
    create_datasets_parser,
    create_documents_parser,
    create_logs_parser,
    create_models_parser,
    create_organizations_parser,
    create_plans_parser,
    create_predictions_parser,
    create_secrets_parser,
    create_transitions_parser,
    create_users_parser,
    create_workflows_parser,
)


def create_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=textwrap.dedent('''
            Command Line Interface for Cradl API, see --help for more info or visit https//docs.cradl.ai. To use tab 
            completion make sure you have global completion activated. See argcomplete docs for more information: 
            https://kislyuk.github.io/argcomplete/
        '''),
    )
    parser.add_argument('--profile')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    subparsers = parser.add_subparsers()

    create_app_clients_parser(subparsers)
    create_assets_parser(subparsers)
    create_datasets_parser(subparsers)
    create_documents_parser(subparsers)
    create_logs_parser(subparsers)
    create_models_parser(subparsers)
    create_organizations_parser(subparsers)
    create_plans_parser(subparsers)
    create_predictions_parser(subparsers)
    create_secrets_parser(subparsers)
    create_transitions_parser(subparsers)
    create_users_parser(subparsers)
    create_workflows_parser(subparsers)

    argcomplete.autocomplete(parser)
    return parser


def set_verbosity(verbose):
    verbosity_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    verbosity = verbosity_levels[min(verbose, len(verbosity_levels) - 1)]
    logging.getLogger().setLevel(verbosity)
    logging.getLogger('las').setLevel(verbosity)


def main():
    parser = create_parser()
    args = vars(parser.parse_args())
    set_verbosity(args.pop('verbose'))
    profile = args.pop('profile', None)

    try:
        cmd = args.pop('cmd')
    except:
        parser.print_help()
        exit(1)

    try:
        if profile:
            credentials = Credentials(*read_from_file(section=profile))
            args['las_client'] = Client(credentials)
        else:
            args['las_client'] = Client()
    except (configparser.NoOptionError, configparser.NoSectionError, MissingCredentials) as e:
        logging.exception(e)
        print('Could not locate credentials.')
        return

    kwargs = {k: v for k, v in args.items() if v != NotProvided}
    if kwargs:
        result = cmd(**kwargs)
        result = json.dumps(result, indent=2) if isinstance(result, dict) else result
        print(result)
    else:
        parser.print_help()
        exit(1)


if __name__ == '__main__':
    main()
