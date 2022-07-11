import pytest
from tests import service, util
from unittest.mock import patch


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


@patch('las.Client.create_secret')
@patch('las.Client.create_asset')
@patch('las.Client.create_dataset')
def test_workflows_create_default(
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
        service.create_model_id()
 ]
    
    create_asset.return_value = {'assetId': service.create_asset_id()}
    create_secret.return_value = {'secretId': service.create_secret_id()}
    create_dataset.return_value = {'datasetId': service.create_dataset_id()}

   
    util.main_parser(parser, client, args)
    

@patch('las.Client.delete_dataset')
@patch('las.Client.delete_transition')
@patch('las.Client.delete_secret')
@patch('las.Client.delete_asset')
@patch('las.Client.create_workflow', side_effect=RuntimeError('Foobar'))
@patch('las.Client.create_secret')
@patch('las.Client.create_asset')
@patch('las.Client.create_dataset')
def test_workflows_create_default_cleanup(
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

    util.main_parser(parser, client, args)
    
    delete_asset.assert_called()
    delete_secret.assert_called()
    delete_transition.assert_called()
    delete_dataset.assert_called()
