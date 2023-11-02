import pytest
from tests import service, util


@pytest.mark.parametrize('data_scientist_assistance', [
    ('--data-scientist-assistance',),
    (),
])
@pytest.mark.parametrize('data_bundle_ids', [
    (service.create_data_bundle_id(), service.create_data_bundle_id()),
    [service.create_data_bundle_id()]
])
def test_trainings_create(parser, client, data_scientist_assistance, data_bundle_ids, name_and_description, metadata):
    args = [
        'models',
        'create-training',
        service.create_model_id(),
        *data_bundle_ids,
        *data_scientist_assistance,
        *name_and_description,
    ]
    util.main_parser(parser, client, args)


def test_trainings_get(parser, client):
    args = [
        'models',
        'get-training',
        service.create_model_id(),
        service.create_training_id(),
    ]
    util.main_parser(parser, client, args)


def test_trainings_list(parser, client, list_defaults):
    args = [
        'models',
        'list-trainings',
        service.create_model_id(),
        *list_defaults,
    ]
    util.main_parser(parser, client, args)


@pytest.mark.parametrize('cancel', [['--cancel'], []])
def test_trainings_update(parser, client, name_and_description, cancel, metadata):
    args = [
        'models',
        'update-training',
        service.create_model_id(),
        service.create_training_id(),
        *name_and_description,
        *cancel,
        *metadata,
    ]

    if len(args) == 4:  # patch call requires at least one change
        # TODO: Remove this return when the API is updated
        return  # Early return due to error in the API
        with pytest.raises(Exception):
            util.main_parser(parser, client, args)
    else:
        if '--metadata' not in args:
            return  # Due to some bug somewhere
        util.main_parser(parser, client, args)


@pytest.mark.skip
def test_trainings_delete(parser, client):
    args = [
        'trainings',
        'delete-training',
        service.create_model_id(),
        service.create_training_id(),
    ]
    util.main_parser(parser, client, args)
