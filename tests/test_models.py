import pytest
from tests import service, util


@pytest.mark.parametrize('metadata', [('--metadata', str(util.metadata_path())), ()])
@pytest.mark.parametrize('preprocess_config', [('-p', str(util.preprocess_config_path())), ()])
def test_models_create(parser, client, metadata, preprocess_config, name_and_description):
    args = [
        'models',
        'create',
        f'{util.field_config_path()}',
        *metadata,
        *name_and_description,
        *preprocess_config,
    ]
    util.main_parser(parser, client, args)


@pytest.mark.parametrize('metadata', [('--metadata', str(util.metadata_path())), ()])
@pytest.mark.parametrize('preprocess_config', [('--preprocess-config', str(util.preprocess_config_path())), ()])
@pytest.mark.parametrize('field_config', [('--field-config', str(util.field_config_path())), ()])
def test_models_update(parser, client, metadata, preprocess_config, name_and_description, field_config):
    args = [
        'models',
        'update',
        service.create_model_id(),
        *metadata,
        *name_and_description,
        *preprocess_config,
        *field_config,
    ]

    if len(args) == 3:  # patch call requires at least one change
        with pytest.raises(Exception):
            util.main_parser(parser, client, args)
    else:
        util.main_parser(parser, client, args)


def test_models_list(parser, client, list_defaults):
    args = [
        'models',
        'list',
        *list_defaults,
    ]
    util.main_parser(parser, client, args)


def test_models_get(parser, client):
    args = [
        'models',
        'get',
        service.create_model_id(),
    ]
    util.main_parser(parser, client, args)


@pytest.mark.skip
def test_models_delete(parser, client):
    args = [
        'models',
        'delete',
        service.create_model_id(),
    ]
    util.main_parser(parser, client, args)
