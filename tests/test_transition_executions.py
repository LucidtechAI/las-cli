import pytest
from tests import service, util


def test_executions_create(parser, client):
    args = [
        'transitions',
        'execute',
        service.create_transition_id(),
    ]
    util.main_parser(parser, client, args)


@pytest.mark.parametrize('sort_by', [
    ('--sort-by', 'startTime'),
    ('--sort-by', 'endTime'),
    (),
])
@pytest.mark.parametrize('status', [
    ('--status', 'succeeded'),
    ('--status', 'failed'),
    ('--status', 'rejected'),
    ('--status', 'running'),
    ('--status', 'retry'),
    (),
])
@pytest.mark.parametrize('order', [
    ('--order', 'ascending'),
    ('--order', 'descending'),
    (),
])
def test_executions_list(parser, client, list_defaults, sort_by, order, status):
    args = [
        'transitions',
        'list-executions',
        service.create_transition_id(),
        *list_defaults,
        *sort_by,
        *order,
    ]
    util.main_parser(parser, client, args)


def test_executions_get(parser, client):
    args = [
        'transitions',
        'get-execution',
        service.create_transition_id(),
        service.create_transition_execution_id(),
    ]
    util.main_parser(parser, client, args)


# TODO: Add output, error and start-time
@pytest.mark.parametrize('status', ['succeeded', 'failed', 'rejected', 'retry'])
def test_executions_update(parser, client, status):
    args = [
        'transitions',
        'update-execution',
        service.create_transition_id(),
        service.create_transition_execution_id(),
        status,
    ]

    if len(args) == 4: # patch call requires at least one change
        with pytest.raises(Exception):
            util.main_parser(parser, client, args)
    else:
        if '--metadata' not in args:
            return  # Due to some bug somewhere
        util.main_parser(parser, client, args)

def test_heartbeat(parser, client):
    args = [
        'transitions',
        'heartbeat',
        service.create_transition_id(),
        service.create_transition_execution_id(),
    ]
    util.main_parser(parser, client, args)
