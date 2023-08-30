import pytest
from tests import service, util


@pytest.mark.parametrize('role_ids', [
    ('--role-ids', service.create_role_id(), service.create_role_id()),
    ('--role-ids', service.create_role_id()),
    (),
])
def test_users_create(parser, client, role_ids):
    args = [
        'users',
        'create',
        service.create_email(),
        service.create_app_client_id(),
        *role_ids,
    ]
    util.main_parser(parser, client, args)
    
    
@pytest.mark.parametrize('role_ids', [
    ('--role-ids', service.create_role_id(), service.create_role_id()),
    ('--role-ids', service.create_role_id()),
    (),
])
def test_users_update(parser, client, role_ids):
    args = [
        'users',
        'update',
        service.create_user_id(),
        *role_ids,
    ]

    if len(args) <= 3:  # patch call requires at least one change
        with pytest.raises(Exception):
            util.main_parser(parser, client, args)
    else:
        util.main_parser(parser, client, args)


def test_users_list(parser, client, list_defaults):
    args = [
        'users',
        'list',
        *list_defaults,
    ]
    util.main_parser(parser, client, args)


@pytest.mark.skip
def test_users_delete(parser, client):
    args = [
        'users',
        'delete',
        service.create_user_id(),
    ]
    util.main_parser(parser, client, args)
