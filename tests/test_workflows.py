import json
from unittest.mock import patch

import pytest
from tests import service, util


@pytest.mark.parametrize('completed_config', [
    ('--completed-config', str(util.transition_parameters_path())),
    ('--completed-config', util.transition_parameters_path().read_text()), 
    ()
])
@pytest.mark.parametrize('error_config', [
    ('--error-config', str(util.error_config_path())),
    ('--error-config', util.error_config_path().read_text()), 
    ()
])
@pytest.mark.parametrize('email_config', [
    ('--email-config', str(util.email_config_path())),
    ('--email-config', util.email_config_path().read_text()), 
    ()
])
@pytest.mark.parametrize('metadata', [
    ('--metadata', str(util.metadata_path())),
    ('--metadata', util.metadata_path().read_text()), 
    ()
])
def test_workflows_create(parser, client, name_and_description, error_config, completed_config, email_config, metadata):
    args = [
        'workflows',
        'create',
        str(util.assets_folder() / 'workflow_specification.json'),
        *name_and_description,
        *error_config,
        *email_config,
        *completed_config,
        *metadata,
    ]
    util.main_parser(parser, client, args)


@pytest.mark.parametrize('completed_config', [
    ('--completed-config', str(util.transition_parameters_path())),
    ('--completed-config', util.transition_parameters_path().read_text()), 
    ()
])
@pytest.mark.parametrize('error_config', [
    ('--error-config', str(util.error_config_path())),
    ('--error-config', util.error_config_path().read_text()), 
    ()
])
@pytest.mark.parametrize('email_config', [
    ('--email-config', str(util.email_config_path())),
    ('--email-config', util.email_config_path().read_text()),
    ('--email-config', 'null'),
    ()
])
@pytest.mark.parametrize('metadata', [
    ('--metadata', str(util.metadata_path())),
    ('--metadata', util.metadata_path().read_text()), 
    ()
])
@pytest.mark.parametrize('status', [
    ('--status', 'development'),
    ('--status', 'production'), 
    ()
])
def test_workflows_update(
    parser, 
    client, 
    name_and_description, 
    error_config, 
    completed_config, 
    email_config, 
    metadata,
    status,
):
    args = [
        'workflows',
        'update',
        service.create_workflow_id(),
        *name_and_description,
        *error_config,
        *email_config,
        *completed_config,
        *metadata,
        *status,
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


@patch('las.Client.create_secret')
@patch('las.Client.create_asset')
@patch('las.Client.create_dataset')
@patch('las.Client.get_model')
@patch('las.Client.create_transition')
@patch('las.Client.create_workflow')
def test_workflows_create_default(
    create_workflow,
    create_transition,
    get_model,
    create_dataset,
    create_asset,
    create_secret,
    parser,
    client,
):
    args = [
        'workflows',
        'create-default',
        'My workflow',
        '--from-model-id',
        service.create_model_id(),
    ]

    create_workflow.return_value = {'workflowId': service.create_workflow_id()}
    create_transition.return_value = {'transitionId': service.create_training_id()}
    create_asset.return_value = {'assetId': service.create_asset_id()}
    create_secret.return_value = {'secretId': service.create_secret_id()}
    create_dataset.return_value = {'datasetId': service.create_dataset_id()}

    get_model.return_value = {
        'fieldConfig': {
            'field1': {'type': 'numeric', 'description': 'Display1'},
            'field2': {'type': 'date', 'description': 'Display2'},
        },
    }

    util.main_parser(parser, client, args)


@patch('las.Client.delete_dataset')
@patch('las.Client.delete_transition')
@patch('las.Client.delete_secret')
@patch('las.Client.delete_asset')
@patch('las.Client.create_workflow', side_effect=RuntimeError('Error while creating workflow! (Intended)'))
@patch('las.Client.create_secret')
@patch('las.Client.create_asset')
@patch('las.Client.create_dataset')
@patch('las.Client.get_model')
@patch('las.Client.create_transition')
def test_workflows_create_default_cleanup(
    create_transition,
    get_model,
    create_dataset,
    create_asset,
    create_secret,
    create_workflow,
    delete_asset,
    delete_secret,
    delete_transition,
    delete_dataset,
    parser,
    client,
):
    args = [
        'workflows',
        'create-default',
        'My workflow',
        '--from-model-id',
        service.create_model_id()
    ]

    create_asset.return_value = {'assetId': service.create_asset_id()}
    create_secret.return_value = {'secretId': service.create_secret_id()}
    create_dataset.return_value = {'datasetId': service.create_dataset_id()}
    create_transition.return_value = {'transitionId': service.create_training_id()}

    get_model.return_value = {
        'fieldConfig': {
            'field1': { 'type': 'numeric', 'description': 'Display1'},
            'field2': { 'type': 'date', 'description': 'Display2'},
        }
    }

    util.main_parser(parser, client, args)

    delete_asset.assert_called()
    delete_secret.assert_called()
    delete_transition.assert_called()
    delete_dataset.assert_called()
