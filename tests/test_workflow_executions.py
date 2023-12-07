import pytest
from tests import service, util


def test_executions_create(parser, client):
    args = [
        'workflows',
        'execute',
        service.create_workflow_id(),
        str(util.metadata_path()),
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
    ('--status', 'error'),
    ('--status', 'error', 'retry'),
    (),
])
@pytest.mark.parametrize('order', [
    ('--order', 'ascending'),
    ('--order', 'descending'),
    (),
])
@pytest.mark.parametrize('from_start_time', [
    ('--from-start-time', '2022-01-01'),
    ('--from-start-time', '3d'),
    (),
])
@pytest.mark.parametrize('to_start_time', [
    ('--to-start-time', '2022-01-01'),
    ('--to-start-time', '3d'),
    (),
])
def test_executions_list(parser, client, list_defaults, sort_by, order, status, from_start_time, to_start_time):
    args = [
        'workflows',
        'list-executions',
        service.create_workflow_id(),
        *list_defaults,
        *sort_by,
        *order,
        *from_start_time,
        *to_start_time,
    ]
    util.main_parser(parser, client, args)


def test_executions_get(parser, client):
    args = [
        'workflows',
        'get-execution',
        service.create_workflow_id(),
        service.create_workflow_execution_id(),
    ]
    util.main_parser(parser, client, args)


@pytest.mark.parametrize('optional_args', [
    ('--next-transition-id', service.create_transition_id()),
    ('--status', 'completed'),
])
def test_executions_update(parser, client, optional_args):
    args = [
        'workflows',
        'update-execution',
        service.create_workflow_id(),
        service.create_workflow_execution_id(),
        *optional_args,
    ]
    util.main_parser(parser, client, args)
