from las import Client


def post_batches(las_client: Client, description):
    description = description or 'default'
    return las_client.post_batches(description)


def create_batches_parser(subparsers):
    parser = subparsers.add_parser('batches')
    subparsers = parser.add_subparsers()

    create_batch_parser = subparsers.add_parser('create')
    create_batch_parser.add_argument('--description')
    create_batch_parser.set_defaults(cmd=post_batches)

    return parser
