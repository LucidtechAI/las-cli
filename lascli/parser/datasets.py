import json
import logging
import os
from collections import Counter
from pathlib import Path
from time import time
from itertools import zip_longest
from functools import partial
from las import Client
from multiprocessing import Pool

from lascli.util import nullable, NotProvided


# See https://docs.python.org/3/library/itertools.html
def group(iterable, group_size, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 4, 'x') --> ABCD EFGx"
    args = [iter(iterable)] * group_size
    return zip_longest(*args, fillvalue=fillvalue)


def post_datasets(las_client: Client, **optional_args):
    return las_client.create_dataset(**optional_args)


def list_datasets(las_client: Client, max_results=None, next_token=None):
    return las_client.list_datasets(max_results=max_results, next_token=next_token)


def update_dataset(las_client: Client, dataset_id, **optional_args):
    return las_client.update_dataset(dataset_id, **optional_args)


def delete_dataset(las_client: Client, dataset_id, delete_documents):
    return las_client.delete_dataset(dataset_id, delete_documents=delete_documents)


def _create_documents_pool(t, client, dataset_id):
    doc, metadata = t
    try:
        client.create_document(content=doc, dataset_id=dataset_id, **metadata)
        return doc, True, None
    except Exception as e:
        return doc, False, str(e)


def upload_batch_to_dataset(
    las_client: Client,
    dataset_id,
    documents,
    chunk_size,
    documents_uploaded,
    documents_failed,
    num_parallel,
):
    log_file = Path(documents_uploaded)
    error_file = Path(documents_failed)
    documents = json.loads(Path(documents).read_text())
    uploaded_files = []
    counter = Counter()

    if log_file.exists():
        uploaded_files = log_file.read_text().splitlines()

    if error_file.exists():
        logging.warning(f'{error_file} exists and will be overwritten')

    with log_file.open('a') as lf, error_file.open('a') as ef:
        pool = Pool(num_parallel or os.cpu_count())
        num_docs = len(documents)
        print(f'start uploading {num_docs} document in chunks of {chunk_size}...')
        start_time = time()

        for n, chunk in enumerate(group(documents, chunk_size)):
            print(f'{(time() - start_time) / 60:.2f}m: {n * chunk_size} docs...')

            fn = partial(_create_documents_pool, client=las_client, dataset_id=dataset_id)
            inp = [(item, documents[item]) for item in chunk if item is not None and item not in uploaded_files]
            results = pool.map(fn, inp)

            for name, uploaded, reason in results:
                if uploaded:
                    lf.write(name + '\n')
                    message = f'successfully uploaded {name}'
                    counter['uploaded'] += 1
                else:
                    ef.write(name + '\n')
                    message = f'failed to upload {name}: {reason}'
                    counter['failed'] += 1

                print(message)

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

    upload_batch_to_dataset_parser = subparsers.add_parser('upload-batch')
    upload_batch_to_dataset_parser.add_argument('dataset_id')
    upload_batch_to_dataset_parser.add_argument('documents', default=False)
    upload_batch_to_dataset_parser.add_argument('--chunk-size', default=100, type=int)
    upload_batch_to_dataset_parser.add_argument('--documents-uploaded', default='.documents_uploaded.log')
    upload_batch_to_dataset_parser.add_argument('--documents-failed', default='.documents_failed.log')
    upload_batch_to_dataset_parser.add_argument('--num-parallel', default=None, type=int)
    upload_batch_to_dataset_parser.set_defaults(cmd=upload_batch_to_dataset)

    return parser
