import pytest
from tests import service, util


@pytest.mark.parametrize('owner', [['--owner', 'foo@lucidtech.io'], []])
def test_plans_list(parser, client, list_defaults, owner):
    args = [
        'plans',
        'list',
        *list_defaults,
        *owner,
    ]
    util.main_parser(parser, client, args)


def test_plans_get(parser, client):
    args = [
        'plans',
        'get',
        service.create_plan_id(),
    ]
    util.main_parser(parser, client, args)
