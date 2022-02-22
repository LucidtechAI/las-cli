import pytest
from tests import service, util


@pytest.mark.parametrize('metadata', [('--metadata', str(util.metadata_path())), ()])
def test_datasets_create(parser, client, metadata, name_and_description):
    args = [
        'datasets',
        'create',
        *metadata,
        *name_and_description,
    ]
    util.main_parser(parser, client, args)


@pytest.mark.parametrize('metadata', [('--metadata', str(util.metadata_path())), ()])
def test_datasets_update(parser, client, metadata, name_and_description):
    args = [
        'datasets',
        'update',
        service.create_dataset_id(),
        *metadata,
        *name_and_description,
    ]

    if len(args) == 3: # patch call requires at least one change
        with pytest.raises(Exception):
            util.main_parser(parser, client, args)
    else:
        util.main_parser(parser, client, args)


def test_datasets_list(parser, client, list_defaults):
    args = [
        'datasets',
        'list',
        *list_defaults,
    ]
    util.main_parser(parser, client, args)


def test_datasets_get(parser, client):
    args = [
        'datasets',
        'get',
        service.create_dataset_id(),
    ]
    util.main_parser(parser, client, args)


@pytest.mark.skip
@pytest.mark.parametrize('delete_documents', [('--delete-documents',), ()])
def test_datasets_delete(parser, client, delete_documents):
    args = [
        'datasets',
        'delete',
        service.create_dataset_id(),
        *delete_documents,
    ]
    util.main_parser(parser, client, args)


@pytest.mark.skip(reason='non-standard implementation')
def test_datasets_create_documents(parser, client):
    args = [
        'datasets',
        'get',
        service.create_dataset_id(),
    ]
    util.main_parser(parser, client, args)
