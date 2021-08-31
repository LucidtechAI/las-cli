import json
import logging
from collections import Counter
from pathlib import Path
from time import time
from itertools import zip_longest
from functools import partial
from las import Client
from concurrent.futures import ThreadPoolExecutor

from lascli.util import nullable, NotProvided


# See https://docs.python.org/3/library/itertools.html
def group(iterable, group_size, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 4, 'x') --> ABCD EFGx"
    args = [iter(iterable)] * group_size
    return zip_longest(*args, fillvalue=fillvalue)


def _create_documents_worker(t, client, dataset_id):
    doc, metadata = t
    try:
        client.create_document(content=doc, dataset_id=dataset_id, **metadata)
        return doc, True, None
    except Exception as e:
        return doc, False, str(e)


def post_datasets(las_client: Client, **optional_args):
    return las_client.create_dataset(**optional_args)


def list_datasets(las_client: Client, max_results=None, next_token=None):
    return las_client.list_datasets(max_results=max_results, next_token=next_token)


def update_dataset(las_client: Client, dataset_id, **optional_args):
    return las_client.update_dataset(dataset_id, **optional_args)


def delete_dataset(las_client: Client, dataset_id, delete_documents):
    return las_client.delete_dataset(dataset_id, delete_documents=delete_documents)


def sync(
    las_client: Client,
    dataset_id,
    documents_json_path,
    chunk_size,
    documents_uploaded,
    documents_failed,
    num_threads,
):
    log_file = Path(documents_uploaded)
    error_file = Path(documents_failed)
    documents = json.loads(Path(documents_json_path).read_text())
    uploaded_files = []
    counter = Counter()

    if log_file.exists():
        uploaded_files = log_file.read_text().splitlines()

    if error_file.exists():
        logging.warning(f'{error_file} exists and will be appended to')

    with log_file.open('a') as lf, error_file.open('a') as ef, ThreadPoolExecutor(max_workers=num_threads) as executor:
        num_docs = len(documents)
        start_time = time()
        print(f'start uploading {num_docs} document in chunks of {chunk_size}...')

        for n, chunk in enumerate(group(documents, chunk_size)):
            fn = partial(_create_documents_worker, client=las_client, dataset_id=dataset_id)
            inp = [(item, documents[item]) for item in chunk if item is not None and item not in uploaded_files]

            for name, uploaded, reason in executor.map(fn, inp):
                if uploaded:
                    lf.write(name + '\n')
                    counter['uploaded'] += 1
                    message = f'successfully uploaded {name}'
                else:
                    ef.write(name + '\n')
                    message = f'failed to upload {name}: {reason}'
                    counter['failed'] += 1

                print(message)

            minutes_spent = (time() - start_time) / 60
            documents_processed = n * chunk_size
            progress = documents_processed / num_docs * 100
            print(f'{minutes_spent:.2f}m: {documents_processed}/{num_docs} docs processed | {progress:.1f}%')

    return dict(counter)


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

    upload_batch_to_dataset_parser = subparsers.add_parser('sync')
    upload_batch_to_dataset_parser.add_argument('dataset_id')
    upload_batch_to_dataset_parser.add_argument(
        'documents_json_path',
        default=False,
        help='json file containing a dictionary with the keys being the path of the actual document, '
             'and the value being keyword arguments that will be used to create that document'
    )
    upload_batch_to_dataset_parser.add_argument('--chunk-size', default=500, type=int)
    upload_batch_to_dataset_parser.add_argument('--documents-uploaded', default='.documents_uploaded.log')
    upload_batch_to_dataset_parser.add_argument('--documents-failed', default='.documents_failed.log')
    upload_batch_to_dataset_parser.add_argument('--num-threads', default=32, type=int)
    upload_batch_to_dataset_parser.set_defaults(cmd=sync)

    return parser
