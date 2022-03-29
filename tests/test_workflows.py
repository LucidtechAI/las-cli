import pytest
from tests import service, util


@pytest.mark.parametrize('completed_config', [('--completed-config', str(util.transition_parameters_path())), ()])
@pytest.mark.parametrize('error_config', [('--error-config', str(util.error_config_path())), ()])
def test_workflows_create(parser, client, name_and_description, error_config, completed_config):
    args = [
        'workflows',
        'create',
        str(util.assets_folder() / 'workflow_specification.json'),
        *name_and_description,
        *error_config,
        *completed_config,
    ]
    util.main_parser(parser, client, args)


@pytest.mark.parametrize('completed_config', [('--completed-config', str(util.transition_parameters_path())), ()])
@pytest.mark.parametrize('error_config', [('--error-config', str(util.error_config_path())), ()])
def test_workflows_update(parser, client, name_and_description, error_config, completed_config):
    args = [
        'workflows',
        'update',
        service.create_workflow_id(),
        *name_and_description,
        *error_config,
        *completed_config,
    ]

    if len(args) == 3:  # patch call requires at least one change
        with pytest.raises(Exception):
            util.main_parser(parser, client, args)
    else:
        util.main_parser(parser, client, args)


def test_workflows_list(parser, client, list_defaults):
    args = [
        'workflows',
        'list',
        *list_defaults,
    ]
    util.main_parser(parser, client, args)


def test_workflows_get(parser, client):
    args = [
        'workflows',
        'get',
        service.create_workflow_id(),
    ]
    util.main_parser(parser, client, args)


@pytest.mark.skip
def test_workflows_delete(parser, client):
    args = [
        'workflows',
        'delete',
        service.create_workflow_id(),
    ]
    util.main_parser(parser, client, args)