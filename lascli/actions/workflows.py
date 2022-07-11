import collections
import json
import os
import requests
import traceback
import uuid

from datetime import datetime
from las import Client
from typing import Optional

from ..util import wrap_output, capture_return


# FIXME: Get this from somewhere else.
COMPONENT_ASSEST_URI = 'https://raw.githubusercontent.com/LucidtechAI/las-docs/master/tutorials/simple-demo/backend/src/Invoice/assets/jsRemoteComponent.js'  

created_ids = collections.defaultdict(list)
 

def create_workflow_spec(
    model_id: str, 
    preprocess_transition_id: str, 
    manual_transition_id: str,
    postprocess_transition_id: str, 
    tag: str,
):
    return {
        'definition': {
            'Comment': f'Auto-generated workflow for model {model_id}. {tag}.',
            'StartAt': 'Preprocess',
            'States': {
                'Preprocess': {
                    'Type': 'Task',
                    'Resource': preprocess_transition_id,
                    'Next': 'CheckValidation'
                },
                'CheckValidation': {
                    'Type': 'Choice',
                    'Choices': [{
                        'Variable': '$.needsValidation',
                        'BooleanEquals': False,
                        'Next': 'Postprocess'
                    }, {
                        'Variable': '$.needsValidation',
                        'BooleanEquals': True,
                        'Next': 'Validate'
                    }]
                },
                'Validate': {
                    'Type': 'Task',
                    'Resource': manual_transition_id,
                    'Next': 'Postprocess'
                },
                'Postprocess': {
                    'Type': 'Task',
                    'Resource': postprocess_transition_id,
                    'End': True
                }
            }
        }
    }
    

def create_field_config(las_client: Client, model_id: str):
    model = las_client.get_model(model_id)
    field_config = model['fieldConfig']

    def transform(field):
        return {
            'type': field_config[field]['type'],
            'display': field_config[field].get('description') or field,
            'confidenceLevels': {
                'automated': 0.95,
                'high': 0.80,
                'medium': 0.5,
                'low': 0.3,
            }
        }

    return {field: transform(field) for field in field_config}
    

@wrap_output(start_msg='Creating secrets ...', end_msg='Done')
@capture_return(dest=created_ids['secrets'])
def create_secrets(las_client: Client, create_tag: str, username: str = None, password: str = None):
    docker_secret = {}
    if username and password:
        docker_secret = las_client.create_secret(
            data={
                'username': username,
                'password': password 
            },
            name='Docker credentials',
            description=create_tag,
        )
        
    cradl_secret = las_client.create_secret(
        data={
            'LAS_CLIENT_ID': las_client.credentials.client_id,
            'LAS_CLIENT_SECRET': las_client.credentials.client_secret,
            'LAS_AUTH_ENDPOINT': las_client.credentials.auth_endpoint,
            'LAS_API_ENDPOINT': las_client.credentials.api_endpoint,
        },
        name='Cradl credentials',
        description=create_tag,
    )
        
    return docker_secret.get('secretId'), cradl_secret['secretId']


@wrap_output(start_msg='Creating remote component and field config asset ...', end_msg='Done')
@capture_return(dest=created_ids['assets'])
def create_assets(las_client: Client, model_id: str, create_tag: str):
    component = las_client.create_asset(
        content=requests.get(COMPONENT_ASSEST_URI).content,
        name='Manual validation component',
        description=create_tag,
    )
    
    field_config = las_client.create_asset(
        content=json.dumps(create_field_config(las_client, model_id)).encode('utf-8'),
        name='Field configuration',
        description=create_tag,
    )

    return component['assetId'], field_config['assetId']


@wrap_output(start_msg='Creating dataset ...', end_msg='Done')
@capture_return(dest=created_ids['datasets'])
def create_dataset(las_client: Client, name: str, create_tag: str):
    dataset = las_client.create_dataset(name=name, description=f'Dataset for {name} model. {create_tag}')
    return dataset['datasetId']
    

@wrap_output(start_msg='Creating transitions ...', end_msg='Done')
@capture_return(dest=created_ids['transitions'])
def create_transitions(
    las_client: Client, 
    cradl_secret_id: str, 
    name: str,
    model_id: str,
    dataset_id: str,
    preprocess_image: str,
    postprocess_image: str,
    field_config_asset_id: str,
    remote_component_asset_id: str,
    create_tag: str, 
    created_ids: dict, 
    docker_secret_id: str = None,
):
    docker_auth_details = {'secretId': docker_secret_id} if docker_secret_id else {}

    common_params = {
        'environmentSecrets': [cradl_secret_id],
        'environment': {
            'MODEL_ID': model_id,
            'FIELD_CONFIG_ASSET_ID': field_config_asset_id,
            'DATASET_ID': dataset_id,
        },
        **docker_auth_details
    }
    
    preprocess = las_client.create_transition(
        transition_type='docker',
        parameters={'imageUrl': preprocess_image, **common_params},
        name=f'Preprocess transition for workflow {name}',
        description=create_tag,
    )
    
    postprocess = las_client.create_transition(
        transition_type='docker',
        parameters={'imageUrl': postprocess_image, **common_params},
        name=f'Postprocess transition for workflow {name}',
        description=create_tag,
    )

    manual = las_client.create_transition(
        transition_type='manual',
        parameters={
            'assets': {
                'jsRemoteComponent': remote_component_asset_id,
                'fieldConfig': field_config_asset_id
            }
        },
        name=name,
        description=create_tag,
    )

    return preprocess['transitionId'], postprocess['transitionId'], manual['transitionId']


def create_default_workflow(las_client: Client, name: str, **optional_args):
    timestamp = datetime.now()
    create_tag = f'Created by CLI at {timestamp.isoformat()} (tag:{uuid.uuid4().hex})'
    model_id = optional_args.get('from_model_id')
    
    if model_id:
        try:
            docker_secret_id, cradl_secret_id = create_secrets(
                las_client=las_client,
                create_tag=create_tag,
                username=optional_args.get('username'),
                password=optional_args.get('password'),
            )

            component_asset_id, field_config_id = create_assets(
                las_client=las_client,
                model_id=model_id,
                create_tag=create_tag,
            )
            
            dataset_id = create_dataset(
                las_client=las_client,
                name=f'Dataset for {name}',
                create_tag=create_tag,
            )

            preprocess_id, postprocess_id, manual_id = create_transitions(
                las_client=las_client,
                cradl_secret_id=cradl_secret_id,
                remote_component_asset_id=component_asset_id,
                field_config_asset_id=field_config_id,
                docker_secret_id=docker_secret_id,
                preprocess_image=optional_args['preprocess_image'],
                postprocess_image=optional_args['postprocess_image'],
                name=name,
                model_id=model_id,
                dataset_id=dataset_id,
                create_tag=create_tag,
                created_ids=created_ids,
            )

            spec = create_workflow_spec(
                model_id=model_id,
                preprocess_transition_id=preprocess_id,
                postprocess_transition_id=postprocess_id,
                manual_transition_id=manual_id,
                tag=create_tag,
            )
            
            workflow = las_client.create_workflow(
                specification=spec,
                name=name,
                description=create_tag,
            )

            print(f'Created workflow {workflow["workflowId"]}')

            return workflow
        except Exception as e:
            traceback.print_exc()

            print('Cleaning up resources ...')
            
            def for_each(fn, resources, msg=None):
                for resource in filter(lambda r: r, resources or []):
                    try:
                        print(f'{msg} ({resource}) ...')
                        fn(resource)
                    except Exception as e:
                        traceback.print_exc(e)

            for_each(las_client.delete_transition, created_ids.get('transitions', []), msg='Deleting transition')
            for_each(las_client.delete_secret, created_ids.get('secrets'), msg='Deleting secret')
            for_each(las_client.delete_asset, created_ids.get('assets'), msg='Deleting asset')
            for_each(las_client.delete_dataset, created_ids.get('datasets'), msg='Deleting dataset')
