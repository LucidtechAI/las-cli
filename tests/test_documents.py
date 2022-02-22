import pytest
from tests import service, util


@pytest.mark.parametrize('dataset_id', [service.optional_argument('dataset'), ()])
@pytest.mark.parametrize('consent_id', [service.optional_argument('consent'), ()])
@pytest.mark.parametrize('content_type', [('--content-type', 'image/jpeg'), ()])
def test_documents_create(parser, client, dataset_id, consent_id, content_type):
    args = [
        'documents',
        'create',
        f'{util.assets_folder()}/example.jpeg',
        *content_type,
        *consent_id,
        *dataset_id,
    ]
    util.main_parser(parser, client, args)


@pytest.mark.parametrize('dataset_id', [service.optional_argument('dataset'), ()])
@pytest.mark.parametrize('consent_id', [service.optional_argument('consent'), ()])
@pytest.mark.parametrize('list_defaults', util.max_results_and_next_token())
def test_documents_list(parser, client, dataset_id, consent_id, list_defaults):
    args = [
        'documents',
        'list',
        *consent_id,
        *dataset_id,
        *list_defaults,
    ]
    util.main_parser(parser, client, args)

@pytest.mark.parametrize('output_content', [('--output-content',), ()])
@pytest.mark.parametrize('download_content', [('--download-content', service.temporary_named_file()), ()])
def test_documents_get(parser, client, output_content, download_content):
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr('base64.b64decode', lambda *args: b'foo')
        args = [
            'documents',
            'get',
            service.create_document_id(),
            *output_content,
            *download_content,
        ]
        util.main_parser(parser, client, args)
