import pytest
from tests import service, util


def secrets_options():
    return [
        ('--secret-data', 'foo=bar', 'baz=5'),
        ('--secret-path', str(util.assets_folder() / 'secret.json')),
    ]


@pytest.mark.parametrize('secret', secrets_options())
def test_secrets_create(parser, client, secret, name_and_description):
    args = [
        'secrets',
        'create',
        *name_and_description,
        *secret,
    ]
    util.main_parser(parser, client, args)


@pytest.mark.parametrize('secret', secrets_options())
def test_secrets_update(parser, client, name_and_description, secret):
    args = [
        'secrets',
        'update',
        service.create_secret_id(),
        *name_and_description,
        *secret,
    ]

    if len(args) == 3:  # patch call requires at least one change
        with pytest.raises(Exception):
            util.main_parser(parser, client, args)
    else:
        util.main_parser(parser, client, args)


def test_secrets_list(parser, client, list_defaults):
    args = [
        'secrets',
        'list',
        *list_defaults,
    ]
    util.main_parser(parser, client, args)


@pytest.mark.skip
def test_secrets_delete(parser, client):
    args = [
        'secrets',
        'delete',
        service.create_secret_id(),
    ]
    util.main_parser(parser, client, args)
