import pytest
from tests import service, util


@pytest.mark.parametrize('metadata', [('--metadata', str(util.metadata_path())), ()])
@pytest.mark.parametrize('preprocess_config', [
    ('-p', str(util.preprocess_config_path())),
    ('--preprocess-config', str(util.preprocess_config_path())),
    ('--preprocess-config', util.preprocess_config_path().read_text()),
    (),
])
@pytest.mark.parametrize('postprocess_config', [
    ('--postprocess-config', str(util.postprocess_config_path())),
    ('--postprocess-config', util.postprocess_config_path().read_text()),
    (),
])
@pytest.mark.parametrize('base_model', [
    ('--base-model', f'{service.create_organization_id()}/{service.create_model_id()}'),
    (),
])
def test_models_create(
    parser, 
    client, 
    metadata, 
    preprocess_config, 
    postprocess_config, 
    name_and_description, 
    base_model,
):
    args = [
        'models',
        'create',
        f'{util.field_config_path()}',
        *metadata,
        *name_and_description,
        *preprocess_config,
        *postprocess_config,
        *base_model,
    ]
    util.main_parser(parser, client, args)


@pytest.mark.parametrize('metadata', [('--metadata', str(util.metadata_path())), ()])
@pytest.mark.parametrize('preprocess_config', [
    ('--preprocess-config', str(util.preprocess_config_path())),
    ('--preprocess-config', util.preprocess_config_path().read_text()),
    (),
])
@pytest.mark.parametrize('postprocess_config', [
    ('--postprocess-config', str(util.postprocess_config_path())),
    ('--postprocess-config', util.postprocess_config_path().read_text()),
    (),
])
@pytest.mark.parametrize('field_config', [('--field-config', str(util.field_config_path())), ()])
def test_models_update(
    parser, 
    client, 
    metadata, 
    preprocess_config, 
    postprocess_config, 
    name_and_description, 
    field_config,
):
    args = [
        'models',
        'update',
        service.create_model_id(),
        *metadata,
        *name_and_description,
        *preprocess_config,
        *postprocess_config,
        *field_config,
    ]

    if len(args) == 3:  # patch call requires at least one change
        with pytest.raises(Exception):
            util.main_parser(parser, client, args)
    else:
        util.main_parser(parser, client, args)


@pytest.mark.parametrize('owner', [
    ('--owner', service.create_organization_id()),
    ('--owner', 'me'),
    (),
])
def test_models_list(parser, client, list_defaults, owner):
    args = [
        'models',
        'list',
        *list_defaults,
        *owner,
    ]
    util.main_parser(parser, client, args)


@pytest.mark.parametrize('statistics_last_n_days', [
    ('--statistics-last-n-days', '14'),
    (),
])
def test_models_get(parser, client, statistics_last_n_days):
    args = [
        'models',
        'get',
        service.create_model_id(),
        *statistics_last_n_days,
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
