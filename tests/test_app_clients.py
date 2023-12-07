import pytest
from tests import service, util


@pytest.mark.parametrize('role_ids', [
    ('--role-ids', service.create_role_id(), service.create_role_id()),
    ('--role-ids', service.create_role_id()),
    (),
])
def test_app_clients_create(parser, client, name_and_description, role_ids):
    args = [
        'app-clients',
        'create',
        *name_and_description,
        *role_ids,
    ]
    util.main_parser(parser, client, args)


@pytest.mark.parametrize('role_ids', [
    ('--role-ids', service.create_role_id(), service.create_role_id()),
    ('--role-ids', service.create_role_id()),
    (),
])
def test_app_clients_create_secret(parser, client, name_and_description, role_ids):
    args = [
        'app-clients',
        'create',
        '--generate-secret',
        '--logout-urls',
        'http://localhost:3030/logout',
        '--login-urls',
        'http://localhost:3030/login',
        '--callback-urls',
        'http://localhost:3030/callback',
        '--default-login-url',
        'http://localhost:3030/login',
        *name_and_description,
        *role_ids,
    ]
    util.main_parser(parser, client, args)


@pytest.mark.parametrize('role_ids', [
    ('--role-ids', service.create_role_id(), service.create_role_id()),
    ('--role-ids', service.create_role_id()),
    (),
])
def test_app_clients_update(parser, client, name_and_description, role_ids):
    args = [
        'app-clients',
        'update',
        service.create_app_client_id(),
        *name_and_description,
        *role_ids,
    ]

    if len(args) <= 3:  # patch call requires at least one change
        with pytest.raises(Exception):
            util.main_parser(parser, client, args)
    else:
        util.main_parser(parser, client, args)


def test_app_clients_get(parser, client):
    args = [
        'app-clients',
        'get',
        service.create_app_client_id(),
    ]
    util.main_parser(parser, client, args)


def test_app_clients_list(parser, client, list_defaults):
    args = [
        'app-clients',
        'list',
        *list_defaults,
    ]
    util.main_parser(parser, client, args)


def test_app_clients_delete(parser, client):
    args = [
        'app-clients',
        'delete',
        service.create_app_client_id(),
    ]
    util.main_parser(parser, client, args)
