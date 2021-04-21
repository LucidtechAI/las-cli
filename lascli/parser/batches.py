from las import Client


def post_batches(las_client: Client, **optional_args):
    return las_client.create_batch(**optional_args)


def list_batches(las_client: Client, max_results=None, next_token=None):
    return las_client.list_batches(max_results=max_results, next_token=next_token)


def create_batches_parser(subparsers):
    parser = subparsers.add_parser('batches')
    subparsers = parser.add_subparsers()

    create_batch_parser = subparsers.add_parser('create')
    create_batch_parser.add_argument('--description')
    create_batch_parser.add_argument('--name')
    create_batch_parser.set_defaults(cmd=post_batches)

    list_batches_parser = subparsers.add_parser('list')
    list_batches_parser.add_argument('--max-results', '-m', type=int, default=None)
    list_batches_parser.add_argument('--next-token', '-n', default=None)
    list_batches_parser.set_defaults(cmd=list_batches)

    return parser
