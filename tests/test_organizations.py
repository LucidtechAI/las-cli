import pytest
from tests import service, util


@pytest.mark.parametrize('payment_method_id', [('--payment-method-id', service.create_payment_method_id()), ()])
def test_organizations_update(parser, client, payment_method_id, name_and_description):
    args = [
        'organizations',
        'update',
        service.create_organization_id(),
        *payment_method_id,
        *name_and_description,
    ]

    if len(args) == 3:  # patch call requires at least one change
        with pytest.raises(Exception):
            util.main_parser(parser, client, args)
    else:
        util.main_parser(parser, client, args)


def test_organizations_get(parser, client):
    args = [
        'organizations',
        'get',
        service.create_organization_id(),
    ]
    util.main_parser(parser, client, args)
