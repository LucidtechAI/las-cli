from las import Client


def list_users(las_client: Client):
    return las_client.list_users()


def get_user(las_client: Client, user_id):
    return las_client.get_user(user_id)


def create_user(las_client: Client, email):
    return las_client.create_user(email)


def delete_user(las_client: Client, user_id):
    return las_client.delete_user(user_id)


def create_users_parser(subparsers):
    parser = subparsers.add_parser('users')
    subparsers = parser.add_subparsers()

    create_user_parser = subparsers.add_parser('create')
    create_user_parser.add_argument('email')
    create_user_parser.set_defaults(cmd=create_user)

    list_users_parser = subparsers.add_parser('list')
    list_users_parser.set_defaults(cmd=list_users)

    get_user_parser = subparsers.add_parser('get')
    get_user_parser.add_argument('user_id')
    get_user_parser.set_defaults(cmd=get_user)

    delete_user_parser = subparsers.add_parser('delete')
    delete_user_parser.add_argument('user_id')
    delete_user_parser.set_defaults(cmd=delete_user)

    return parser
