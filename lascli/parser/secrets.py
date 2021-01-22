from las import Client

from lascli.util import nullable, NotProvided


def list_secrets(las_client: Client, max_results, next_token):
    return las_client.list_secrets(max_results=max_results, next_token=next_token)


def create_secret(las_client: Client, data, **optional_args):
    secret_data = {}
    for data_entry in data:
        key, val = data_entry.split('=', 1)
        secret_data[key] = val
    return las_client.create_secret(secret_data, **optional_args)


def update_secret(las_client: Client, secret_id, data, **optional_args):
    secret_data = {}
    for data_entry in data:
        key, val = data_entry.split('=', 1)
        secret_data[key] = val
    return las_client.update_secret(secret_id, data=secret_data, **optional_args)


def create_secrets_parser(subparsers):
    parser = subparsers.add_parser('secrets')
    subparsers = parser.add_subparsers()

    list_secrets_parser = subparsers.add_parser('list')
    list_secrets_parser.add_argument('--max-results', '-m', type=int, default=None)
    list_secrets_parser.add_argument('--next-token', '-n', type=str, default=None)
    list_secrets_parser.set_defaults(cmd=list_secrets)

    create_secret_parser = subparsers.add_parser('create')
    create_secret_parser.add_argument('data', metavar='KEY=VALUE', nargs='+')
    create_secret_parser.add_argument('--name')
    create_secret_parser.add_argument('--description')
    create_secret_parser.set_defaults(cmd=create_secret)

    update_secret_parser = subparsers.add_parser('update')
    update_secret_parser.add_argument('secret_id')
    update_secret_parser.add_argument('--data', metavar='KEY=VALUE', nargs='+')
    update_secret_parser.add_argument('--name', type=nullable, default=NotProvided)
    update_secret_parser.add_argument('--description', type=nullable, default=NotProvided)
    update_secret_parser.set_defaults(cmd=update_secret)

    return parser
