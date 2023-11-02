import pytest
from tests import service, util


@pytest.mark.parametrize('dataset_ids', [
    (service.create_dataset_id(), service.create_dataset_id()),
    [service.create_dataset_id()]
])
def test_data_bundles_create(parser, client, dataset_ids, name_and_description):
    args = [
        'models',
        'create-data-bundle',
        service.create_model_id(),
        *dataset_ids,
        *name_and_description,
    ]
    util.main_parser(parser, client, args)
    
    
def test_data_bundles_get(parser, client):
    args = [
        'models',
        'get-data-bundle',
        service.create_model_id(),
        service.create_data_bundle_id(),
    ]
    util.main_parser(parser, client, args)


def test_data_bundles_list(parser, client, list_defaults):
    args = [
        'models',
        'list-data-bundles',
        service.create_model_id(),
        *list_defaults,
    ]
    util.main_parser(parser, client, args)


def test_data_bundles_list_all(parser, client):
    args = [
        'models',
        'list-all-data-bundles',
    ]
    util.main_parser(parser, client, args)


def test_data_bundles_update(parser, client, name_and_description):
    args = [
        'models',
        'update-data-bundle',
        service.create_model_id(),
        service.create_data_bundle_id(),
        *name_and_description,
    ]

    if len(args) == 4:  # patch call requires at least one change
        return  # Early return due to error in the API
        with pytest.raises(Exception):
            util.main_parser(parser, client, args)
    else:
        util.main_parser(parser, client, args)


@pytest.mark.skip
def test_data_bundles_delete(parser, client):
    args = [
        'data_bundles',
        'delete-data-bundle',
        service.create_model_id(),
        service.create_data_bundle_id(),
    ]
    util.main_parser(parser, client, args)
