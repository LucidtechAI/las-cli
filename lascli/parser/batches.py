from las import Client

from lascli.util import nullable, NotProvided


def post_batches(las_client: Client, **optional_args):
    return las_client.create_batch(**optional_args)


def list_batches(las_client: Client, max_results=None, next_token=None):
    return las_client.list_batches(max_results=max_results, next_token=next_token)


def update_batch(las_client: Client, batch_id, **optional_args):
    return las_client.update_batch(batch_id, **optional_args)


def delete_batch(las_client: Client, batch_id, delete_documents):
    return las_client.delete_batch(batch_id, delete_documents=delete_documents)


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

    update_batch_parser = subparsers.add_parser('update')
    update_batch_parser.add_argument('batch_id')
    update_batch_parser.add_argument('--name', type=nullable, default=NotProvided)
    update_batch_parser.add_argument('--description', type=nullable, default=NotProvided)
    update_batch_parser.set_defaults(cmd=update_batch)

    delete_batch_parser = subparsers.add_parser('delete')
    delete_batch_parser.add_argument('batch_id')
    delete_batch_parser.add_argument('--delete-documents', action='store_true', default=False)
    delete_batch_parser.set_defaults(cmd=delete_batch)

    return parser
