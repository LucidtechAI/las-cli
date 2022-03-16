import argparse
import csv
import json
import logging
import yaml
from argparse import ArgumentDefaultsHelpFormatter
from collections import Counter
from pathlib import Path
from time import time
from itertools import zip_longest
from functools import partial
from las import Client
from concurrent.futures import ThreadPoolExecutor

from lascli.util import NotProvided, nullable, json_path

# See https://docs.python.org/3/library/itertools.html
def group(iterable, group_size, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 4, 'x') --> ABCD EFGx"
    args = [iter(iterable)] * group_size
    return zip_longest(*args, fillvalue=fillvalue)


def _create_documents_worker(t, client, dataset_id):
    doc, metadata = t
    if isinstance(metadata, list):
        # Assuming that the metadata is the explicit ground truth
        metadata = {'ground_truth': metadata}
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


def get_dataset(las_client: Client, dataset_id):
    return las_client.get_dataset(dataset_id)


def delete_dataset(las_client: Client, dataset_id, delete_documents):
    return las_client.delete_dataset(dataset_id, delete_documents=delete_documents)


def parse_csv(csv_path, delimiter=','):
    documents = {}
    with csv_path.open() as csv_fp:
        reader = csv.DictReader(csv_fp, delimiter=delimiter)
        name_field = reader.fieldnames[0]
        print(f'Assuming the document file names can be read from the column named {name_field}')

        for row in reader:
            doc_name = row.pop(name_field)
            documents[doc_name] = [{'label': label, 'value': value} for label, value in row.items()]

    return documents


def create_documents(
    las_client: Client,
    dataset_id,
    input_path,
    chunk_size,
    documents_uploaded,
    documents_failed,
    num_threads,
    ground_truth_encoding,
    delimiter,
):
    log_file = Path(documents_uploaded)
    error_file = Path(documents_failed)
    counter = Counter()

    if error_file.exists():
        logging.warning(f'{error_file} exists and will be appended to')

    if input_path.is_file():
        if input_path.suffix == '.json':
            documents = json.loads(Path(input_path).read_text(encoding=ground_truth_encoding))
        elif input_path.suffix == '.csv':
            documents = parse_csv(input_path, delimiter=delimiter)
    elif input_path.is_dir():
        documents = {}
        possible_suffixes = {'.json': json.loads, '.yaml': yaml.safe_load, '.yml': yaml.safe_load}
        anti_pattern = '|'.join([f'!{suffix}' for suffix in possible_suffixes])

        with error_file.open('a') as ef:
            for document_path in input_path.glob(f'*[{anti_pattern}]'):
                for suffix, parser in possible_suffixes.items():
                    ground_truth_path = document_path.with_suffix(suffix)
                    if ground_truth_path.is_file():
                        try:
                            ground_truth = parser(ground_truth_path.read_text(encoding=ground_truth_encoding))
                            documents[str(document_path)] = {'ground_truth': ground_truth}
                            break
                        except Exception as e:
                            ef.write(str(ground_truth_path) + '\n')
                            counter['failed'] += 1
                            print(f'failed to parse {ground_truth_path}: {e}')

    else:
        raise ValueError(f'input_path must be a path to either a json-file or a folder, {input_path} is not valid')

    uploaded_files = []

    if log_file.exists():
        uploaded_files = log_file.read_text().splitlines()

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
            documents_processed = counter['uploaded'] + counter['failed']
            progress = documents_processed / num_docs * 100
            print(f'{minutes_spent:.2f}m: {documents_processed}/{num_docs} docs processed | {progress:.1f}%')

    return dict(counter)


def create_datasets_parser(subparsers):
    parser = subparsers.add_parser('datasets')
    subparsers = parser.add_subparsers()

    create_dataset_parser = subparsers.add_parser('create')
    create_dataset_parser.add_argument('--description')
    create_dataset_parser.add_argument('--name')
    create_dataset_parser.add_argument(
        '--metadata',
        type=json_path,
        help='path to json file with whatever you need, maximum limit 4kB',
    )
    create_dataset_parser.set_defaults(cmd=post_datasets)

    list_datasets_parser = subparsers.add_parser('list')
    list_datasets_parser.add_argument('--max-results', '-m', type=int, default=None)
    list_datasets_parser.add_argument('--next-token', '-n', default=None)
    list_datasets_parser.set_defaults(cmd=list_datasets)

    get_dataset_parser = subparsers.add_parser('get')
    get_dataset_parser.add_argument('dataset_id')
    get_dataset_parser.set_defaults(cmd=get_dataset)

    update_dataset_parser = subparsers.add_parser('update')
    update_dataset_parser.add_argument('dataset_id')
    update_dataset_parser.add_argument('--name', type=nullable, default=NotProvided)
    update_dataset_parser.add_argument('--description', type=nullable, default=NotProvided)
    update_dataset_parser.add_argument(
        '--metadata',
        type=json_path,
        help='path to json file with whatever you need, maximum limit 4kB',
    )
    update_dataset_parser.set_defaults(cmd=update_dataset)

    delete_dataset_parser = subparsers.add_parser('delete')
    delete_dataset_parser.add_argument('dataset_id')
    delete_dataset_parser.add_argument('--delete-documents', action='store_true', default=False)
    delete_dataset_parser.set_defaults(cmd=delete_dataset)

    upload_batch_to_dataset_parser = subparsers.add_parser(
        'create-documents',
        formatter_class=argparse.RawTextHelpFormatter,
    )
    upload_batch_to_dataset_parser.add_argument('dataset_id')
    upload_batch_to_dataset_parser.add_argument(
        'input_path',
        default=False,
        type=Path,
        help='The input path can be provided in two ways: \n'
             '1. Path to a folder of documents (.jpg, .png, .pdf, .tiff) '
             'and corresponding ground truths (.json, .yaml, .yml) with the same file name \n'
             '2. Path to a json file containing a dictionary with the keys being the path of the actual document, '
             'and the value being keyword arguments that will be used to create that document \n'
             '3. Path to a csv file where each row contains information about one document, '
             'and the paths to the documents in the first column.'
    )
    upload_batch_to_dataset_parser.add_argument('--chunk-size', default=500, type=int)
    upload_batch_to_dataset_parser.add_argument(
        '--documents-uploaded',
        default='.documents_uploaded.log',
        help='path to file used for caching progress (default: %(default)s)',
    )
    upload_batch_to_dataset_parser.add_argument(
        '--documents-failed',
        default='.documents_failed.log',
        help='path to file used to store the documents that failed (default: %(default)s)',
    )
    upload_batch_to_dataset_parser.add_argument('--num-threads', default=32, type=int, help='Number of threads to use')
    upload_batch_to_dataset_parser.add_argument(
        '--ground-truth-encoding',
        default=None,
        help='Which encoding to use for the ground truth parsing',
    )
    upload_batch_to_dataset_parser.add_argument(
        '--delimiter',
        default=',',
        help='delimiter to use if parsing a csv file',
    )
    upload_batch_to_dataset_parser.set_defaults(cmd=create_documents)

    return parser
