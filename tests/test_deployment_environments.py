import pytest
from tests import service, util


@pytest.mark.parametrize('owner', [['--owner', service.create_organization_id()], []])
def test_plans_list(parser, client, list_defaults, owner):
    args = [
        'deployment-environments',
        'list',
        *list_defaults,
        *owner,
    ]
    util.main_parser(parser, client, args)


def test_plans_get(parser, client):
    args = [
        'deployment-environments',
        'get',
        service.create_plan_id(),
    ]
    util.main_parser(parser, client, args)
