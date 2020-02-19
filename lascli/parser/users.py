from las import Client


def get_user(las_client: Client, user_id):
    return las_client.get_user(user_id)


def patch_user(las_client: Client, user_id, consent_hash):
    return las_client.update_user(user_id, consent_hash)


def create_users_parser(subparsers):
    parser = subparsers.add_parser('users')
    subparsers = parser.add_subparsers()

    get_user_parser = subparsers.add_parser('get')
    get_user_parser.add_argument('user_id')
    get_user_parser.set_defaults(cmd=get_user)

    update_user_parser = subparsers.add_parser('update')
    update_user_parser.add_argument('user_id')
    update_user_parser.add_argument('consent_hash')
    update_user_parser.set_defaults(cmd=patch_user)

    return parser
