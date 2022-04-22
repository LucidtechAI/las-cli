import pytest
from tests import service, util


def test_payment_methods_create(parser, client, name_and_description):
    args = [
        'payment-methods',
        'create',
        *name_and_description,
    ]
    util.main_parser(parser, client, args)


def test_payment_methods_update(parser, client, name_and_description):
    args = [
        'payment-methods',
        'update',
        service.create_payment_method_id(),
        *name_and_description,
    ]

    if len(args) == 3:  # patch call requires at least one change
        with pytest.raises(Exception):
            util.main_parser(parser, client, args)
    else:
        util.main_parser(parser, client, args)


def test_payment_methods_list(parser, client, list_defaults):
    args = [
        'payment-methods',
        'list',
        *list_defaults,
    ]
    util.main_parser(parser, client, args)


def test_payment_methods_get(parser, client):
    args = [
        'payment-methods',
        'get',
        service.create_payment_method_id(),
    ]
    util.main_parser(parser, client, args)


@pytest.mark.skip
def test_payment_methods_delete(parser, client, delete_documents):
    args = [
        'payment-methods',
        'delete',
        service.create_payment_method_id(),
        *delete_documents,
    ]
    util.main_parser(parser, client, args)
