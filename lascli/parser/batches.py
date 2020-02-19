from las import Client


def post_batches(las_client: Client, description):
    return las_client.create_batch(description)


def create_batches_parser(subparsers):
    parser = subparsers.add_parser('batches')
    subparsers = parser.add_subparsers()

    create_batch_parser = subparsers.add_parser('create')
    create_batch_parser.add_argument('--description', default='default')
    create_batch_parser.set_defaults(cmd=post_batches)

    return parser
