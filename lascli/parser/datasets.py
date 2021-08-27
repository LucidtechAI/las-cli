import json
from pathlib import Path

from las import Client

from lascli.util import nullable, NotProvided


def post_datasets(las_client: Client, **optional_args):
    return las_client.create_dataset(**optional_args)


def list_datasets(las_client: Client, max_results=None, next_token=None):
    return las_client.list_datasets(max_results=max_results, next_token=next_token)


def update_dataset(las_client: Client, dataset_id, **optional_args):
    return las_client.update_dataset(dataset_id, **optional_args)


def delete_dataset(las_client: Client, dataset_id, delete_documents):
    return las_client.delete_dataset(dataset_id, delete_documents=delete_documents)


def upload_batch_to_dataset(
    las_client: Client,
    dataset_id,
    documents,
    chunk_size,
    documents_uploaded,
    documents_failed,
):
    documents = json.loads(Path(documents).read_text())
    return las_client.batch_create_document(
        documents,
        dataset_id=dataset_id,
        chunk_size=chunk_size,
        log_file=documents_uploaded,
        error_file=documents_failed,
    )


def create_datasets_parser(subparsers):
    parser = subparsers.add_parser('datasets')
    subparsers = parser.add_subparsers()

    create_dataset_parser = subparsers.add_parser('create')
    create_dataset_parser.add_argument('--description')
    create_dataset_parser.add_argument('--name')
    create_dataset_parser.set_defaults(cmd=post_datasets)

    list_datasets_parser = subparsers.add_parser('list')
    list_datasets_parser.add_argument('--max-results', '-m', type=int, default=None)
    list_datasets_parser.add_argument('--next-token', '-n', default=None)
    list_datasets_parser.set_defaults(cmd=list_datasets)

    update_dataset_parser = subparsers.add_parser('update')
    update_dataset_parser.add_argument('dataset_id')
    update_dataset_parser.add_argument('--name', type=nullable, default=NotProvided)
    update_dataset_parser.add_argument('--description', type=nullable, default=NotProvided)
    update_dataset_parser.set_defaults(cmd=update_dataset)

    delete_dataset_parser = subparsers.add_parser('delete')
    delete_dataset_parser.add_argument('dataset_id')
    delete_dataset_parser.add_argument('--delete-documents', action='store_true', default=False)
    delete_dataset_parser.set_defaults(cmd=delete_dataset)

    upload_batch_to_dataset_parser = subparsers.add_parser('upload-batch')
    upload_batch_to_dataset_parser.add_argument('dataset_id')
    upload_batch_to_dataset_parser.add_argument('documents', default=False)
    upload_batch_to_dataset_parser.add_argument('--chunk-size', default=100)
    upload_batch_to_dataset_parser.add_argument('--documents-uploaded', default='.documents_uploaded.log')
    upload_batch_to_dataset_parser.add_argument('--documents-failed', default='.documents_failed.log')
    upload_batch_to_dataset_parser.set_defaults(cmd=upload_batch_to_dataset)

    return parser
