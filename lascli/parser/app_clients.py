from las import Client


def create_app_client(las_client: Client, generate_secret, logout_urls, callback_urls, **optional_args):
    return las_client.create_app_client(
        generate_secret=generate_secret,
        logout_urls=logout_urls,
        callback_urls=callback_urls,
        **optional_args,
    )


def list_app_clients(las_client: Client, max_results=None, next_token=None):
    return las_client.list_app_clients(max_results=max_results, next_token=next_token)


def delete_app_client(las_client: Client, app_client_id):
    return las_client.delete_app_client(app_client_id)


def create_app_clients_parser(subparsers):
    parser = subparsers.add_parser('app-clients')
    subparsers = parser.add_subparsers()

    create_app_client_parser = subparsers.add_parser('create')
    create_app_client_parser.add_argument('--name')
    create_app_client_parser.add_argument('--description')
    create_app_client_parser.add_argument('--generate-secret', action='store_true', default=False)
    create_app_client_parser.add_argument('--logout-urls', nargs='+')
    create_app_client_parser.add_argument('--callback-urls', nargs='+')
    create_app_client_parser.set_defaults(cmd=create_app_client)

    list_app_clients_parser = subparsers.add_parser('list')
    list_app_clients_parser.add_argument('--max-results', '-m', type=int, default=None)
    list_app_clients_parser.add_argument('--next-token', '-n', default=None)
    list_app_clients_parser.set_defaults(cmd=list_app_clients)

    delete_app_client_parser = subparsers.add_parser('delete')
    delete_app_client_parser.add_argument('app_client_id')
    delete_app_client_parser.set_defaults(cmd=delete_app_client)

    return parser