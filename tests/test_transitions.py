import pytest
from tests import service, util


@pytest.mark.parametrize('transition_type,parameters', [
    ('docker', ('--parameters', str(util.transition_parameters_path()))),
    ('manual', ()),
])
@pytest.mark.parametrize('in_schema', [('--in-schema', str(util.schema_path())), ()])
@pytest.mark.parametrize('out_schema', [('--out-schema', str(util.schema_path())), ()])
def test_transitions_create(parser, client, transition_type, in_schema, out_schema, name_and_description, parameters):
    args = [
        'transitions',
        'create',
        transition_type,
        *in_schema,
        *out_schema,
        *name_and_description,
    ]
    util.main_parser(parser, client, args)



@pytest.mark.parametrize('in_schema', [('--in-schema', str(util.schema_path())), ()])
@pytest.mark.parametrize('out_schema', [('--out-schema', str(util.schema_path())), ()])
def test_transitions_update(
    parser,
    client,
    in_schema,
    out_schema,
    name_and_description,
):
    args = [
        'transitions',
        'update',
        service.create_transition_id(),
        *in_schema,
        *out_schema,
        *name_and_description,
    ]

    if len(args) == 3:  # patch call requires at least one change
        with pytest.raises(Exception):
            util.main_parser(parser, client, args)
    else:
        util.main_parser(parser, client, args)


@pytest.mark.parametrize('assets', [('--assets', str(util.assets_folder() / 'assets.json')), ()])
def test_transitions_update_manual(
    parser,
    client,
    assets,
):
    args = [
        'transitions',
        'update',
        service.create_transition_id(),
        *assets,
    ]

    if len(args) == 3:  # patch call requires at least one change
        with pytest.raises(Exception):
            util.main_parser(parser, client, args)
    else:
        util.main_parser(parser, client, args)
        

@pytest.mark.parametrize('image_url', [('--image-url', 'image:url'), ()])
@pytest.mark.parametrize('secret_id', [
    ('--secret-id', service.create_secret_id()),
    ('--secret-id', 'null'),
    (),
])
@pytest.mark.parametrize('cpu', [
    ('--cpu', '256'),
    (),
])
@pytest.mark.parametrize('memory', [
    ('--memory', '512'),
    ('--memory', '1024'),
    (),
])
@pytest.mark.parametrize('environment', [
    ('--environment', str(util.assets_folder() / 'secret.json')),
    ('--environment', 'null'),
    (),
])
@pytest.mark.parametrize('environment_secrets', [
    ('--environment-secrets', service.create_secret_id(), service.create_secret_id()),
    ('--environment-secrets', service.create_secret_id()),
    ('--environment-secrets', 'null'),
    (),
])
def test_transitions_update_docker(
    parser,
    client,
    image_url,
    secret_id,
    cpu,
    memory,
    environment,
    environment_secrets,
):
    args = [
        'transitions',
        'update',
        service.create_transition_id(),
        *image_url,
        *secret_id,
        *cpu,
        *memory,
        *environment,
        *environment_secrets,
    ]

    if len(args) == 3:  # patch call requires at least one change
        with pytest.raises(Exception):
            util.main_parser(parser, client, args)
    else:
        util.main_parser(parser, client, args)


@pytest.mark.parametrize('transition_type', [
    ('--transition-type', 'docker'),
    ('--transition-type', 'manual'),
    (),
])
def test_transitions_list(parser, client, transition_type, list_defaults):
    args = [
        'transitions',
        'list',
        *transition_type,
        *list_defaults,
    ]
    util.main_parser(parser, client, args)


def test_transitions_get(parser, client):
    args = [
        'transitions',
        'get',
        service.create_transition_id(),
    ]
    util.main_parser(parser, client, args)


@pytest.mark.skip
def test_transitions_delete(parser, client):
    args = [
        'transitions',
        'delete',
        service.create_transition_id(),
    ]
    util.main_parser(parser, client, args)
