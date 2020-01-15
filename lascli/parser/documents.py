import filetype
import pathlib

from las import Client


def post_documents(las_client: Client, document_path, content_type, consent_id, batch_id):
    content = pathlib.Path(document_path).read_bytes()

    if not content_type:
        guessed_type = filetype.guess(content)
        assert guessed_type, 'Could not determine content type of document. ' \
                             'Please provide it manually with --content-type'
        content_type = guessed_type.mime

    consent_id = consent_id or 'default'
    return las_client.post_documents(content, content_type, consent_id, batch_id)


def post_feedback(las_client: Client, document_id, fields):
    feedback = [f.split('=', 1) for f in fields]
    feedback = [{'label': k, 'value': v} for k, v in feedback]
    return las_client.post_document_id(document_id, feedback)


def create_documents_parser(subparsers):
    parser = subparsers.add_parser('documents')
    subparsers = parser.add_subparsers()

    create_document_parser = subparsers.add_parser('create')
    create_document_parser.add_argument('document_path')
    create_document_parser.add_argument('--content-type')
    create_document_parser.add_argument('--consent-id')
    create_document_parser.add_argument('--batch-id')
    create_document_parser.set_defaults(cmd=post_documents)

    feedback_document_parser = subparsers.add_parser('feedback')
    feedback_document_parser.add_argument('document_id')
    feedback_document_parser.add_argument('--fields', metavar='KEY=VALUE', nargs='+')
    feedback_document_parser.set_defaults(cmd=post_feedback)

    return parser
