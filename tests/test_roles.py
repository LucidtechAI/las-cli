import pytest
from tests import service, util


def test_roles_list(parser, client, list_defaults):
    args = [
        'roles',
        'list',
        *list_defaults,
    ]
    util.main_parser(parser, client, args)


def test_roles_get(parser, client):
    args = [
        'roles',
        'get',
        service.create_role_id(),
    ]
    util.main_parser(parser, client, args)
