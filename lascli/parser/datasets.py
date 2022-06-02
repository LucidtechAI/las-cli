import argparse
import base64
import csv
import json
import logging
from argparse import ArgumentDefaultsHelpFormatter
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
from itertools import zip_longest
from pathlib import Path
from time import time

import filetype
import yaml
from filetype.types.archive import Pdf
from filetype.types.image import Png, Jpeg, Tiff
from las import Client
from yaml.parser import ParserError

from lascli.util import NotProvided, nullable, json_path


def group(iterable, group_size):
    # See https://docs.python.org/3/library/itertools.html
    # group('ABCDEFG', 4) --> ABCD EFG
    args = [iter(iterable)] * group_size
    return map(lambda g: list(filter(bool, g)), zip_longest(*args, fillvalue=None))


def _create_documents_worker(document, client, dataset_id):
    document_path, metadata = document
    if isinstance(metadata, list):
        # Assuming that the metadata is the explicit ground truth
        metadata = {'ground_truth': metadata}
    try:
        client.create_document(content=document_path, dataset_id=dataset_id, **metadata)
        return document_path, True, None
    except Exception as e:
        return document_path, False, str(e)


def _get_document_worker(las_client: Client, document_id, output_dir):
    try:
        document = las_client.get_document(document_id)
        document_content = base64.b64decode(document['content'])
        document_content_file_name = f'{document["documentId"]}.{filetype.guess_extension(document_content)}'
        (output_dir / document_content_file_name).write_bytes(document_content)
        document_ground_truth_file_name = f'{document["documentId"]}.json'
        (output_dir / document_ground_truth_file_name).write_text(json.dumps(document.get('groundTruth', []), indent=2))
        return document
    except Exception as e:
        print(f'Failed to download document {document_id}')
        return None


def _list_all_documents_in_dataset(las_client: Client, dataset_id):
    list_response = las_client.list_documents(dataset_id=dataset_id)
    yield from list_response['documents']
    next_token = list_response.get('nextToken')

    while next_token:
        list_response = las_client.list_documents(dataset_id=dataset_id, next_token=next_token)
        yield from list_response['documents']
        next_token = list_response.get('nextToken')


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


def parse_csv(csv_path, ground_truth_encoding, delimiter=','):
    documents = {}
    with csv_path.open(encoding=ground_truth_encoding) as csv_fp:
        reader = csv.DictReader(csv_fp, delimiter=delimiter)
        name_field = reader.fieldnames[0]
        print(f'Assuming the document file names can be read from the column named {name_field}')

        for row in reader:
            doc_name = row.pop(name_field)
            documents[doc_name] = [{'label': label, 'value': value} for label, value in row.items()]

    return documents


def read_json(path, encoding):
    try:
        return json.loads(path.read_text(encoding))
    except (UnicodeDecodeError, json.JSONDecodeError):
        pass


def read_yaml(path, encoding):
    try:
        return yaml.safe_load(path.read_text(encoding))
    except (UnicodeDecodeError, ParserError):
        pass


def read_ground_truth(path, encoding):
    return read_json(path, encoding) or read_yaml(path, encoding)


def _documents_from_dir(src_dir, accepted_document_types, ground_truth_encoding):
    grouped_paths = defaultdict(list)

    for path in src_dir.iterdir():
        if path.is_file():
            grouped_paths[path.stem].append(path)

    for name, paths in grouped_paths.items():
        document_path = None
        ground_truth_path = None

        for path in paths:
            kind = filetype.guess(path)
            if not kind and path.suffix.lower() in ['.json', '.yaml', '.yml']:
                if ground_truth_path:
                    print(f'Ground truth file for {name} already found (Old: {ground_truth_path} New: {path})')
                ground_truth_path = path
            elif not kind:
                continue
            elif any(isinstance(kind, document_type) for document_type in accepted_document_types):
                if document_path:
                    print(f'Document file for {name} already found (Old: {document_path} New: {path})')
                document_path = path

        if not document_path:
            print(f'Missing document file for {name}')
        if not ground_truth_path:
            print(f'Missing ground truth file for {name}')
        if document_path and ground_truth_path:
            yield (str(document_path), read_ground_truth(ground_truth_path, ground_truth_encoding))


def _documents_from_file(input_path, delimiter, ground_truth_encoding):
    documents = {}

    if input_path.suffix.lower() == '.json':
        documents = read_json(input_path, ground_truth_encoding)
    elif input_path.suffix.lower() == '.csv':
        documents = parse_csv(input_path, ground_truth_encoding, delimiter=delimiter)

    for name in documents:
        yield (name, documents[name])


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
    use_cache,
):
    log_file = Path(documents_uploaded)
    error_file = Path(documents_failed)
    counter = Counter()

    if input_path.is_file():
        documents = _documents_from_file(input_path, delimiter, ground_truth_encoding)
    elif input_path.is_dir():
        documents = _documents_from_dir(input_path, [Pdf, Jpeg, Png, Tiff], ground_truth_encoding)
    else:
        raise ValueError(f'input_path must be a path to either a json-file or a folder, {input_path} is not valid')

    uploaded_files = set()

    if use_cache:
        mode = 'a'
        if log_file.exists():
            uploaded_files = set(log_file.read_text().splitlines())
    else:
        mode = 'w'

    with log_file.open(mode) as lf, error_file.open('w') as ef, ThreadPoolExecutor(max_workers=num_threads) as executor:
        fn = partial(_create_documents_worker, client=las_client, dataset_id=dataset_id)
        start_time = time()

        for chunk in group(documents, chunk_size):
            for name, uploaded, reason in executor.map(fn, filter(lambda d: d[0] not in uploaded_files, chunk)):
                if uploaded:
                    lf.write(name + '\n')
                    counter['uploaded'] += 1
                    message = f'successfully uploaded {name}'
                else:
                    ef.write(name + '\n')
                    message = f'failed to upload {name}: {reason}'
                    counter['failed'] += 1

                print(message)

            step_time = time() - start_time
            minutes = int(step_time // 60)
            seconds = int(step_time % 60)
            documents_processed = counter['uploaded'] + counter['failed']
            print(f'{minutes}m{seconds}s: {documents_processed} docs processed')

    return dict(counter)


def get_documents(las_client: Client, dataset_id, output_dir, num_threads, chunk_size):
    already_downloaded = set()
    if output_dir.exists():
        for path in output_dir.iterdir():
            already_downloaded.add(path.stem)
        print(f'Found {len(already_downloaded)} documents already downloaded')
    else:
        output_dir.mkdir()

    not_downloaded = lambda document: document['documentId'] not in already_downloaded
    print(f'Downloading documents in dataset {dataset_id} to {output_dir}')

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        start_time = time()
        documents = filter(not_downloaded, _list_all_documents_in_dataset(las_client, dataset_id))
        for chunk in group(documents, chunk_size):
            futures = []

            for document in chunk:
                futures.append(executor.submit(_get_document_worker, las_client, document['documentId'], output_dir))

            for future in as_completed(futures):
                document = future.result()
                if document:
                    already_downloaded.add(document['documentId'])

            step_time = time() - start_time
            minutes = int(step_time // 60)
            seconds = int(step_time % 60)
            print(f'{minutes}m{seconds}s: {len(already_downloaded)} downloaded')

    return {'Total downloaded documents': len(already_downloaded)}


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

    create_documents_parser = subparsers.add_parser(
        'create-documents',
        formatter_class=argparse.RawTextHelpFormatter,
    )
    create_documents_parser.add_argument('dataset_id')
    create_documents_parser.add_argument(
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
    create_documents_parser.add_argument('--chunk-size', default=500, type=int)
    create_documents_parser.add_argument(
        '--documents-uploaded',
        default='.documents_uploaded.log',
        help='path to file used for caching progress (default: %(default)s)',
    )
    create_documents_parser.add_argument(
        '--documents-failed',
        default='.documents_failed.log',
        help='path to file used to store the documents that failed (default: %(default)s)',
    )
    create_documents_parser.add_argument('--num-threads', default=32, type=int, help='Number of threads to use')
    create_documents_parser.add_argument(
        '--ground-truth-encoding',
        default=None,
        help='Which encoding to use for the ground truth parsing',
    )
    create_documents_parser.add_argument(
        '--delimiter',
        default=',',
        help='delimiter to use if parsing a csv file',
    )
    create_documents_parser.add_argument(
        '--use-cache',
        action='store_true',
        help='Use cached data from last time this command was executed in this folder.',
    )
    create_documents_parser.set_defaults(cmd=create_documents)

    get_documents_parser = subparsers.add_parser('get-documents')
    get_documents_parser.add_argument('dataset_id')
    get_documents_parser.add_argument('output_dir', type=Path, help='Path to download directory')
    get_documents_parser.add_argument('--num-threads', default=32, type=int, help='Number of threads to use')
    get_documents_parser.add_argument('--chunk-size', default=100, type=int)
    get_documents_parser.set_defaults(cmd=get_documents)

    return parser
