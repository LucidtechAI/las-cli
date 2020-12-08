from las import Client


def list_models(las_client: Client, max_results, next_token):
    return las_client.list_models(max_results=max_results, next_token=next_token)


def create_models_parser(subparsers):
    parser = subparsers.add_parser('models')
    subparsers = parser.add_subparsers()

    list_models_parser = subparsers.add_parser('list')
    list_models_parser.add_argument('--max-results', '-m', type=int, default=None)
    list_models_parser.add_argument('--next-token', '-n', type=str, default=None)
    list_models_parser.set_defaults(cmd=list_models)

    return parser
