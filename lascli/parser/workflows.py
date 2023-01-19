import argparse
import datetime
import json
import pathlib
import textwrap

import dateparser
from las import Client

from lascli.util import nullable, NotProvided, json_path
from lascli.actions import workflows


def list_workflows(las_client: Client, **optional_args):
    return las_client.list_workflows(**optional_args)


def create_workflow(las_client: Client, specification, **optional_args):
    return las_client.create_workflow(specification, **optional_args)


def get_workflow(las_client: Client, workflow_id):
    return las_client.get_workflow(workflow_id)


def update_workflow(las_client: Client, workflow_id, **optional_args):
    return las_client.update_workflow(workflow_id, **optional_args)


def execute_workflow(las_client: Client, workflow_id, path):
    content = json.loads(pathlib.Path(path).read_text())
    return las_client.execute_workflow(workflow_id, content)


def list_workflow_executions(las_client: Client, workflow_id, **optional_args):
    return las_client.list_workflow_executions(workflow_id, **optional_args)


def delete_workflow(las_client: Client, workflow_id):
    return las_client.delete_workflow(workflow_id)


def get_workflow_execution(las_client: Client, workflow_id, execution_id):
    return las_client.get_workflow_execution(workflow_id, execution_id)


def update_workflow_execution(las_client: Client, workflow_id, execution_id, next_transition_id):
    return las_client.update_workflow_execution(workflow_id, execution_id, next_transition_id)


def delete_workflow_execution(las_client: Client, workflow_id, execution_id):
    return las_client.delete_workflow_execution(workflow_id, execution_id)


def execute_default_workflow(las_client: Client, workflow_id, dataset_id):
    list_response = las_client.list_documents(dataset_id=dataset_id)
    documents = list_response['documents']
    while next_token := list_response.get('nextToken'):
        list_response = las_client.list_documents(dataset_id=dataset_id, next_token=next_token)
        documents.extend(list_response['documents'])

    for document in documents:
        input_content = {'documentId': document['documentId']}
        print(f'Execution workflow: {workflow_id} with input: {input_content}')
        las_client.execute_workflow(workflow_id, input_content)

    return 'Success'


def create_workflows_parser(subparsers):
    parser = subparsers.add_parser('workflows')
    subparsers = parser.add_subparsers()

    list_workflows_parser = subparsers.add_parser('list')
    list_workflows_parser.add_argument('--max-results', '-m', type=int)
    list_workflows_parser.add_argument('--next-token', '-n', type=str)
    list_workflows_parser.set_defaults(cmd=list_workflows)

    create_workflow_parser = subparsers.add_parser('create')
    create_workflow_parser.add_argument('specification', type=json_path, help='path to specification')
    create_workflow_parser.add_argument('--name')
    create_workflow_parser.add_argument('--description')
    create_workflow_parser.add_argument(
        '--error-config',
        type=json_path,
        help='path to the error configuration for the workflow',
    )
    create_workflow_parser.add_argument(
        '--completed-config',
        type=json_path,
        help='path to the execution completed configuration for the workflow',
    )
    create_workflow_parser.set_defaults(cmd=create_workflow)

    update_workflow_parser = subparsers.add_parser('update')
    update_workflow_parser.add_argument('workflow_id')
    update_workflow_parser.add_argument('--name', type=nullable(str), default=NotProvided)
    update_workflow_parser.add_argument('--description', type=nullable(str), default=NotProvided)
    update_workflow_parser.add_argument(
        '--error-config',
        type=json_path,
        help='path to the error configuration for the workflow',
    )
    update_workflow_parser.add_argument(
        '--completed-config',
        type=json_path,
        help='path to the execution completed configuration for the workflow',
    )
    update_workflow_parser.set_defaults(cmd=update_workflow)

    execute_workflow_parser = subparsers.add_parser('execute')
    execute_workflow_parser.add_argument('workflow_id')
    execute_workflow_parser.add_argument('path', help='path to json-file with input to the first state of the workflow')
    execute_workflow_parser.set_defaults(cmd=execute_workflow)

    list_executions_parser = subparsers.add_parser('list-executions')
    list_executions_parser.add_argument('workflow_id')
    list_executions_parser.add_argument('--status', '-s', nargs='+', help='Only return those with the given status')
    list_executions_parser.add_argument('--order')
    list_executions_parser.add_argument('--sort-by')
    list_executions_parser.add_argument('--max-results', '-m', type=int)
    list_executions_parser.add_argument('--next-token', '-n', type=str)
    list_executions_parser.add_argument('--from-start-time', type=dateparser.parse)
    list_executions_parser.add_argument('--to-start-time', type=dateparser.parse)
    list_executions_parser.set_defaults(cmd=list_workflow_executions)

    get_workflow_parser = subparsers.add_parser('get')
    get_workflow_parser.add_argument('workflow_id')
    get_workflow_parser.set_defaults(cmd=get_workflow)

    delete_workflow_parser = subparsers.add_parser('delete')
    delete_workflow_parser.add_argument('workflow_id')
    delete_workflow_parser.set_defaults(cmd=delete_workflow)

    get_workflow_execution_parser = subparsers.add_parser('get-execution')
    get_workflow_execution_parser.add_argument('workflow_id')
    get_workflow_execution_parser.add_argument('execution_id')
    get_workflow_execution_parser.set_defaults(cmd=get_workflow_execution)

    update_workflow_execution_parser = subparsers.add_parser('update-execution')
    update_workflow_execution_parser.add_argument('workflow_id')
    update_workflow_execution_parser.add_argument('execution_id')
    update_workflow_execution_parser.add_argument(
        'next_transition_id',
        help='use las:transition:commons-failed to end an execution',
    )
    update_workflow_execution_parser.set_defaults(cmd=update_workflow_execution)

    delete_workflow_execution_parser = subparsers.add_parser('delete-execution')
    delete_workflow_execution_parser.add_argument('workflow_id')
    delete_workflow_execution_parser.add_argument('execution_id')
    delete_workflow_execution_parser.set_defaults(cmd=delete_workflow_execution)

    create_default_workflow_parser = subparsers.add_parser(
        'create-default',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=textwrap.dedent('''
            Create a workflow that adds ground truth to documents using predictions from a model with help from a
            (human) operator if necessary. Execute the workflow with a single documentId. Example input JSON: 
            {"documentId": "las:document:<abc>"}
        '''),
    )
    create_default_action = create_default_workflow_parser.add_mutually_exclusive_group(required=False)
    create_default_action.add_argument('--from-model-id', help='The model to generate the workflow for')
    create_default_workflow_parser.add_argument('name', help='Name of the workflow')
    create_default_workflow_parser.add_argument(
        '--preprocess-image',
        default='lucidtechai/preprocess:v2',
        help='Docker image for the preprocessor',
    )
    create_default_workflow_parser.add_argument(
        '--postprocess-image',
        default='lucidtechai/postprocess:v2',
        help='Docker image for the postprocessor',
    )
    create_default_workflow_parser.set_defaults(cmd=workflows.create_default_workflow)

    execute_default_workflow_parser = subparsers.add_parser(
        'execute-default',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Execute a default workflow on each document in a dataset',
    )
    execute_default_workflow_parser.add_argument('workflow_id')
    execute_default_workflow_parser.add_argument('dataset_id')
    execute_default_workflow_parser.set_defaults(cmd=execute_default_workflow)

    return parser
