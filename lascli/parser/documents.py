import filetype
import logging
import pathlib
import base64

from las import Client


def get_document(las_client: Client, document_id, download_content):
    document_resp = las_client.get_document_id(document_id)
    content = document_resp['content']

    if download_content:
        logging.info(f'Downloading content to {download_content}')
        binary = base64.b64decode(content)
        pathlib.Path(download_content).write_bytes(binary)

    return {**document_resp, 'content': document_resp['content'][:10] + '... [TRUNCATED]'}


def get_documents(las_client: Client, batch_id, consent_id):
    return las_client.get_documents(batch_id, consent_id)


def post_documents(las_client: Client, document_path, content_type, consent_id, batch_id, fields):
    content = pathlib.Path(document_path).read_bytes()

    if not content_type:
        guessed_type = filetype.guess(content)
        assert guessed_type, 'Could not determine content type of document. ' \
                             'Please provide it manually with --content-type'
        content_type = guessed_type.mime

    consent_id = consent_id or 'default'

    if fields:
        feedback = [f.split('=', 1) for f in fields]
        feedback = [{'label': k, 'value': v} for k, v in feedback]
        return las_client.post_documents(content, content_type, consent_id, batch_id, feedback)
    else:
        return las_client.post_documents(content, content_type, consent_id, batch_id)


def post_feedback(las_client: Client, document_id, fields):
    feedback = [f.split('=', 1) for f in fields]
    feedback = [{'label': k, 'value': v} for k, v in feedback]
    return las_client.post_document_id(document_id, feedback)


def create_documents_parser(subparsers):
    parser = subparsers.add_parser('documents')
    subparsers = parser.add_subparsers()

    get_document_parser = subparsers.add_parser('get')
    get_document_parser.add_argument('document_id')
    get_document_parser.add_argument('-d', '--download-content')
    get_document_parser.set_defaults(cmd=get_document)

    list_documents_parser = subparsers.add_parser('list')
    list_documents_parser.add_argument('--batch-id')
    list_documents_parser.add_argument('--consent-id')
    list_documents_parser.set_defaults(cmd=get_documents)

    create_document_parser = subparsers.add_parser('create')
    create_document_parser.add_argument('document_path')
    create_document_parser.add_argument('--content-type')
    create_document_parser.add_argument('--consent-id')
    create_document_parser.add_argument('--batch-id')
    create_document_parser.add_argument('--fields', metavar='KEY=VALUE', nargs='+')
    create_document_parser.set_defaults(cmd=post_documents)

    feedback_document_parser = subparsers.add_parser('feedback')
    feedback_document_parser.add_argument('document_id')
    feedback_document_parser.add_argument('--fields', metavar='KEY=VALUE', nargs='+')
    feedback_document_parser.set_defaults(cmd=post_feedback)

    return parser
