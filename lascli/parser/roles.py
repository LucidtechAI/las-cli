from datetime import datetime
from las import Client


def list_roles(las_client: Client, **optional_args):
    return las_client.list_roles(**optional_args)


def get_role(las_client: Client, role_id):
    return las_client.get_role(role_id)


def create_roles_parser(subparsers):
    parser = subparsers.add_parser('roles')
    subparsers = parser.add_subparsers()

    get_role_parser = subparsers.add_parser('get')
    get_role_parser.add_argument('role_id')
    get_role_parser.set_defaults(cmd=get_role)

    list_roles_parser = subparsers.add_parser('list')
    list_roles_parser.add_argument('--max-results', '-m', type=int, default=None)
    list_roles_parser.add_argument('--next-token', '-n', type=str, default=None)
    list_roles_parser.set_defaults(cmd=list_roles)
    return parser
