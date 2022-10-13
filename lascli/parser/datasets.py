import argparse
import base64
import csv
import hashlib
import json
import logging
import textwrap
from argparse import ArgumentDefaultsHelpFormatter
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from functools import partial
from itertools import zip_longest
from pathlib import Path
from time import time
from uuid import uuid4

import filetype
import yaml
from filetype.types.archive import Pdf
from filetype.types.image import Png, Jpeg, Tiff
from las import Client
from las.client import NotFound
from yaml.parser import ParserError

from lascli.util import NotProvided, nullable, json_path


def group(iterable, group_size):
    # See https://docs.python.org/3/library/itertools.html
    # group('ABCDEFG', 4) --> ABCD EFG
    args = [iter(iterable)] * group_size
    return map(lambda g: filter(bool, g), zip_longest(*args, fillvalue=None))


def _cache_dir():
    cache_dir = Path.home() / '.lucidtech' / 'cache'
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def _create_document(client, document_content, dataset_id, attributes):
    document_id = client.create_document(
        content=document_content,
        dataset_id=dataset_id,
        **attributes,
    )['documentId']
    document_path = attributes['metadata']['originalFilePath']
    message = f'Successfully uploaded {document_path} %s ground_truth'
    print(message % ('with' if 'ground_truth' in attributes else 'without'))
    return document_id


def _create_documents_worker(
    document_path,
    ground_truth,
    client,
    dataset_id,
    ground_truth_encoding,
    already_uploaded,
):
    attributes = {'metadata': {'originalFilePath': str(document_path)}}

    if ground_truth:
        attributes['ground_truth'] = ground_truth
        serialized_ground_truth = json.dumps(ground_truth, separators=(',', ':'), sort_keys=True).encode()
        ground_truth_digest = hashlib.md5(serialized_ground_truth).hexdigest()
    else:
        ground_truth_digest = None

    document_content = document_path.read_bytes()
    document_digest = hashlib.md5(document_content).hexdigest()

    try:
        if document_digest in already_uploaded:
            document_id = already_uploaded[document_digest]['document_id']
            cached_ground_truth_digest = already_uploaded[document_digest]['ground_truth_digest']
            new_ground_truth = ground_truth_digest and ground_truth_digest != cached_ground_truth_digest
            if new_ground_truth:
                try:
                    client.update_document(document_id, dataset_id=dataset_id, **attributes)
                    print(f'Successfully updated {document_path} with ground_truth')
                except NotFound as e:
                    print(f'Document {document_id} not found, creating new document')
                    document_id = _create_document(
                        client=client,
                        document_content=document_content,
                        dataset_id=dataset_id,
                        attributes=attributes,
                    )
            else:
                print(f'Already uploaded. Skipping')
        else:
            document_id = _create_document(
                client=client,
                document_content=document_content,
                dataset_id=dataset_id,
                attributes=attributes,
            )
        already_uploaded[document_digest] = {
            'document_id': document_id,
            'ground_truth_digest': ground_truth_digest,
        }
        return document_id, document_digest, ground_truth_digest
    except Exception as e:
        print(f'failed to upload {document_path}: {e}')
        return None, document_digest, ground_truth_digest


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
    if not path:
        return
    return read_json(path, encoding) or read_yaml(path, encoding)


def _is_acceptable_file_type(path, acceptable_file_types):
    if not path.exists():
        return False
    kind = filetype.guess(path)
    return any(isinstance(kind, file_type) for file_type in acceptable_file_types)


def _documents_from_dir(src_dir, accepted_document_types, ground_truth_encoding):
    grouped_paths = defaultdict(list)

    for path in src_dir.iterdir():
        if path.is_file():
            grouped_paths[path.stem].append(path)

    for name, paths in grouped_paths.items():
        document_path = None
        ground_truth_path = None

        for path in paths:
            if path.suffix.lower() in ['.json', '.yaml', '.yml']:
                if ground_truth_path:
                    print(f'Ground truth file for {name} already found (Old: {ground_truth_path} New: {path})')
                ground_truth_path = path
            elif _is_acceptable_file_type(path, accepted_document_types):
                if document_path:
                    print(f'Document file for {name} already found (Old: {document_path} New: {path})')
                document_path = path

        if document_path:
            yield document_path, read_ground_truth(ground_truth_path, ground_truth_encoding)
        elif ground_truth_path:
            print(f'Missing document file for {ground_truth_path}')


def find_document_path(document_path, acceptable_document_types):
    if _is_acceptable_file_type(document_path, acceptable_document_types):
        return document_path

    for parent in reversed(document_path.parents):
        new_document_path = document_path.relative_to(parent)
        if _is_acceptable_file_type(new_document_path, acceptable_document_types):
            return new_document_path


def read_csv(path, document_path_column, accepted_document_types, delimiter, encoding):
    with path.open('r') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=delimiter)
        for row in reader:
            document_path = find_document_path(Path(row.pop(document_path_column)), accepted_document_types)
            if document_path:
                yield document_path, [{'label': k, 'value': v} for k, v in row.items()]
            else:
                print(f'Document {document_path} is not one of the accepted document types {accepted_document_types}')


def _documents_from_file(src_file, document_path_column, accepted_document_types, delimiter, ground_truth_encoding):
    if src_file.suffix == '.csv':
        yield from read_csv(
            path=src_file,
            document_path_column=document_path_column,
            accepted_document_types=accepted_document_types,
            delimiter=delimiter,
            encoding=ground_truth_encoding,
        )
    else:
        print('Only CSV file or directory is supported. Aborting.')
        exit(1)


@contextmanager
def cache(dataset_id, input_path, no_cache):
    cache_file = _cache_dir() / hashlib.md5(dataset_id.encode()).hexdigest()
    already_uploaded = defaultdict(dict)

    if cache_file.exists():
        if no_cache:
            cache_file.unlink()
        else:
            for line in cache_file.read_text().splitlines():
                try:
                    document_id, document_digest, ground_truth_digest = line.split(' ')
                    already_uploaded[document_digest] = {
                        'document_id': document_id,
                        'ground_truth_digest': ground_truth_digest if ground_truth_digest != '-' else None,
                    }
                except ValueError:
                    pass

    with cache_file.open('a') as cache_fp:
        yield already_uploaded, cache_fp


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
    document_path_column,
    no_cache,
):
    accepted_document_types = [Pdf, Jpeg, Png, Tiff]
    if input_path.is_file():
        documents = _documents_from_file(
            src_file=input_path,
            document_path_column=document_path_column,
            accepted_document_types=accepted_document_types,
            delimiter=delimiter,
            ground_truth_encoding=ground_truth_encoding,
        )
    elif input_path.is_dir():
        documents = _documents_from_dir(
            src_dir=input_path,
            accepted_document_types=accepted_document_types,
            ground_truth_encoding=ground_truth_encoding,
        )
    else:
        raise ValueError(f'input_path must be a path to a file or directory. {input_path} is not valid')

    counter = Counter()
    with cache(dataset_id, input_path, no_cache) as (already_uploaded, cache_fp), ThreadPoolExecutor(max_workers=num_threads) as executor:
        fn = partial(
            _create_documents_worker,
            client=las_client,
            dataset_id=dataset_id,
            ground_truth_encoding=ground_truth_encoding,
            already_uploaded=already_uploaded,
        )
        start_time = time()
        for chunk in group(documents, chunk_size):
            for document_id, document_digest, ground_truth_digest in executor.map(fn, *zip(*chunk)):
                if document_id:
                    cache_fp.write(f'{document_id} {document_digest} {ground_truth_digest or "-"}\n')
                    counter['uploaded'] += 1
                else:
                    counter['failed'] += 1
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
    else:
        output_dir.mkdir()

    already_downloaded_from_dataset = set()
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        documents = []
        for document in _list_all_documents_in_dataset(las_client, dataset_id):
            if document['documentId'] in already_downloaded:
                already_downloaded_from_dataset.add(document['documentId'])
            else:
                documents.append(document)
        print(f'Found {len(already_downloaded_from_dataset)} documents already downloaded')

        start_time = time()
        print(f'Downloading documents in dataset {dataset_id} to {output_dir}')
        for chunk in group(documents, chunk_size):
            futures = []

            for document in chunk:
                futures.append(executor.submit(_get_document_worker, las_client, document['documentId'], output_dir))

            for future in as_completed(futures):
                document = future.result()
                if document:
                    already_downloaded_from_dataset.add(document['documentId'])

            step_time = time() - start_time
            minutes = int(step_time // 60)
            seconds = int(step_time % 60)
            print(f'{minutes}m{seconds}s: {len(already_downloaded_from_dataset)} downloaded')

    return {'Total downloaded documents': len(already_downloaded_from_dataset)}


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
    update_dataset_parser.add_argument('--name', type=nullable(str), default=NotProvided)
    update_dataset_parser.add_argument('--description', type=nullable(str), default=NotProvided)
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
        help=textwrap.dedent(
            'The input path can be provided in two ways: \n'
            '1. Path to a folder of documents (.jpeg, .png, .pdf, .tiff) and corresponding ground truths (.json, .yaml, '
            '.yml) with the same file name \n'
            '2. Path to a csv file where each row contains ground truth values for the document and one column '
            '(specified by --document-path-column) contains the path to the document (.jpeg, .png, .pdf, .tiff) for '
            'that row.'
        ),
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
        '--document-path-column',
        default='document_path',
        help='Column in which the document path is specified if parsing a csv file',
    )
    create_documents_parser.add_argument(
        '--no-cache',
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
