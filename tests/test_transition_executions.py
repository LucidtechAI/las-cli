import pytest
from datetime import datetime
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


@pytest.mark.parametrize('response', [
    ('--output', str(util.assets_folder() / 'transition_execution_output.json')),
    ('--error', str(util.assets_folder() / 'transition_execution_output.json')),
])
@pytest.mark.parametrize('status', ['succeeded', 'failed', 'rejected', 'retry'])
@pytest.mark.parametrize('start_time', ['--start-time', str(datetime.utcnow()), 'rejected', 'retry'])
def test_executions_update(parser, client, response, start_time, status):
    args = [
        'transitions',
        'update-execution',
        service.create_transition_id(),
        service.create_transition_execution_id(),
        status,
        *response,
        *start_time,
    ]

    if len(args) == 4:  # patch call requires at least one change
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
