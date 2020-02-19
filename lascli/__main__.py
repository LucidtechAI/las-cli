#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import argparse
import argcomplete
import inspect
import logging
import json

from las import Client, Credentials
from las.credentials import read_from_file

from .parser import (create_batches_parser, create_documents_parser, create_users_parser, create_predictions_parser,
                     create_consents_parser)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile')
    subparsers = parser.add_subparsers()

    create_batches_parser(subparsers)
    create_documents_parser(subparsers)
    create_users_parser(subparsers)
    create_predictions_parser(subparsers)
    create_consents_parser(subparsers)

    argcomplete.autocomplete(parser)
    return parser


def args_to_kwargs(args):
    try:
        params = inspect.signature(args.cmd).parameters
        return {p: vars(args)[p] for p in params}
    except AttributeError:
        return {}


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.profile:
        credentials = Credentials(*read_from_file(section=args.profile))
        args.las_client = Client(credentials)
    else:
        args.las_client = Client()
    kwargs = args_to_kwargs(args)

    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger('las').setLevel(logging.INFO)

    if kwargs:
        print(json.dumps(args.cmd(**kwargs), indent=2))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
