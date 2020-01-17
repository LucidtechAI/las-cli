from las import Client


def patch_user(las_client: Client, user_id, consent_hash):
    return las_client.patch_user_id(user_id, consent_hash)


def create_users_parser(subparsers):
    parser = subparsers.add_parser('users')
    subparsers = parser.add_subparsers()

    update_user_parser = subparsers.add_parser('update')
    update_user_parser.add_argument('user_id')
    update_user_parser.add_argument('consent_hash')
    update_user_parser.set_defaults(cmd=patch_user)

    return parser
