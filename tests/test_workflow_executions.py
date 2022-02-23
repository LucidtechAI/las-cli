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
def test_executions_list(parser, client, list_defaults, sort_by, order, status):
    args = [
        'workflows',
        'list-executions',
        service.create_workflow_id(),
        *list_defaults,
        *sort_by,
        *order,
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


def test_executions_update(parser, client):
    args = [
        'workflows',
        'update-execution',
        service.create_workflow_id(),
        service.create_workflow_execution_id(),
        service.create_transition_id(),
    ]
    util.main_parser(parser, client, args)
