import pytest
from tests import service, util


@pytest.mark.parametrize('dataset_id', service.optional_resource_id('dataset'))
@pytest.mark.parametrize('consent_id', service.optional_resource_id('consent'))
@pytest.mark.parametrize('content_type', [('--content-type', 'image/jpeg'), ()])
@pytest.mark.parametrize('ground_truth', util.ground_truth_options())
def test_documents_create(parser, client, dataset_id, consent_id, content_type, metadata, ground_truth):
    args = [
        'documents',
        'create',
        f'{util.assets_folder()}/example.jpeg',
        *content_type,
        *consent_id,
        *dataset_id,
        *metadata,
        *ground_truth,
    ]
    util.main_parser(parser, client, args)


@pytest.mark.parametrize('dataset_id', service.optional_resource_id('dataset'))
@pytest.mark.parametrize('metadata', [('--metadata', str(util.metadata_path())), ()])
@pytest.mark.parametrize('ground_truth', util.ground_truth_options())
def test_documents_update(parser, client, dataset_id, metadata, ground_truth):
    args = [
        'documents',
        'update',
        service.create_document_id(),
        *dataset_id,
        *metadata,
        *ground_truth,
    ]

    if len(args) == 3:  # patch call requires at least one change
        with pytest.raises(Exception):
            util.main_parser(parser, client, args)
    else:
        util.main_parser(parser, client, args)


@pytest.mark.parametrize('dataset_id', service.optional_resource_id('dataset'))
@pytest.mark.parametrize('consent_id', service.optional_resource_id('consent'))
@pytest.mark.parametrize('sort_by', [('--sort-by', 'createdTime')])
@pytest.mark.parametrize('order', [('--order', 'ascending'), ('--order', 'descending')])
def test_documents_list(parser, client, dataset_id, consent_id, list_defaults, sort_by, order):
    args = [
        'documents',
        'list',
        *consent_id,
        *dataset_id,
        *list_defaults,
        *sort_by,
        *order,
    ]
    util.main_parser(parser, client, args)


@pytest.mark.parametrize('output_content', [('--output-content',), ()])
@pytest.mark.parametrize('download_content', [('--download-content', service.temporary_named_file()), ()])
@pytest.mark.parametrize('width', [('--width', '100'), ()])
@pytest.mark.parametrize('height', [('--height', '100'), ()])
@pytest.mark.parametrize('page', [('--page', '1'), ()])
@pytest.mark.parametrize('density', [('--density', '100'), ()])
@pytest.mark.parametrize('rotation', [('--rotation', '90'), ()])
@pytest.mark.parametrize('quality', [('--quality', 'low'), ()])
def test_documents_get(
    parser, 
    client, 
    output_content, 
    download_content, 
    width, 
    height, 
    page, 
    density, 
    rotation, 
    quality,
):
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr('base64.b64decode', lambda *args: b'foo')
        args = [
            'documents',
            'get',
            service.create_document_id(),
            *output_content,
            *width,
            *height,
            *page,
            *density,
            *rotation,
            *download_content,
            *quality,
        ]
        util.main_parser(parser, client, args)


def test_documents_delete(parser, client):
    args = [
        'documents',
        'delete',
        service.create_document_id(),
    ]
    util.main_parser(parser, client, args)


@pytest.mark.parametrize('dataset_id', service.optional_resource_id('dataset'))
@pytest.mark.parametrize('consent_id', service.optional_resource_id('consent'))
def test_documents_delete_all(parser, client, consent_id, dataset_id, list_defaults):
    args = [
        'documents',
        'delete-all',
        *consent_id,
        *dataset_id,
        *list_defaults,
    ]
    util.main_parser(parser, client, args)
