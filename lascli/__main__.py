#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import argparse
import configparser
import inspect
import json
import logging

import argcomplete

from las import Client, Credentials
from las.credentials import MissingCredentials, read_from_file

from .parser import (
    create_assets_parser, create_batches_parser, create_documents_parser,
    create_models_parser, create_predictions_parser, create_secrets_parser,
    create_transitions_parser, create_users_parser, create_workflows_parser,
)


COMMON_ARGS = ['profile', 'verbose', 'cmd']


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    subparsers = parser.add_subparsers()

    create_assets_parser(subparsers)
    create_batches_parser(subparsers)
    create_documents_parser(subparsers)
    create_models_parser(subparsers)
    create_predictions_parser(subparsers)
    create_secrets_parser(subparsers)
    create_transitions_parser(subparsers)
    create_users_parser(subparsers)
    create_workflows_parser(subparsers)

    argcomplete.autocomplete(parser)
    return parser


def nullify(value):
    if isinstance(value, str) and value == 'null':
        return None
    return value


def parse_args(args):
    specified_args = {k: v for k, v in vars(args).items() if v is not None and k not in COMMON_ARGS}
    parsed_args = {k: nullify(v) for k, v in specified_args.items()}
    return parsed_args


def set_verbosity(verbose):
    verbosity_levels = [logging.CRITICAL, logging.WARNING, logging.DEBUG]
    verbosity = verbosity_levels[min(verbose, len(verbosity_levels) - 1)]
    logging.getLogger().setLevel(verbosity)
    logging.getLogger('las').setLevel(verbosity)


def main():
    parser = create_parser()
    args = parser.parse_args()
    set_verbosity(args.verbose)

    try:
        if args.profile:
            credentials = Credentials(*read_from_file(section=args.profile))
            args.las_client = Client(credentials)
        else:
            args.las_client = Client()
    except (configparser.NoOptionError, configparser.NoSectionError, MissingCredentials) as e:
        logging.exception(e)
        print('Could not locate credentials.')
        return

    kwargs = parse_args(args)
    if kwargs:
        print(json.dumps(args.cmd(**kwargs), indent=2))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
