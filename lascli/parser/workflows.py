import datetime
import json
import pathlib
import textwrap
from argparse import RawTextHelpFormatter

import dateparser
from las import Client

from lascli.util import nullable, NotProvided, json_path, json_or_json_path
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


def update_workflow_execution(las_client: Client, workflow_id, execution_id, next_transition_id, status):
    return las_client.update_workflow_execution(workflow_id, execution_id, next_transition_id=next_transition_id, status=status)


def delete_workflow_execution(las_client: Client, workflow_id, execution_id):
    return las_client.delete_workflow_execution(workflow_id, execution_id)


def create_workflows_parser(subparsers):
    parser = subparsers.add_parser('workflows')
    subparsers = parser.add_subparsers()

    list_workflows_parser = subparsers.add_parser('list')
    list_workflows_parser.add_argument('--max-results', '-m', type=int)
    list_workflows_parser.add_argument('--next-token', '-n', type=str)
    list_workflows_parser.set_defaults(cmd=list_workflows)

    create_workflow_parser = subparsers.add_parser('create', formatter_class=RawTextHelpFormatter)
    create_workflow_parser.add_argument('specification', type=json_path, help='path to specification')
    create_workflow_parser.add_argument('--name')
    create_workflow_parser.add_argument('--description')
    create_workflow_parser.add_argument(
        '--email-config',
        type=json_or_json_path,
        help=textwrap.dedent('''
            Path or inline JSON with configuration to enable email input to workflow. The required secretId must have
            permissions to call POST /workflows/:id/executions
            {
                "secretId": string,                 (required)
                "allowedOrigins": list[str],        (optional, list of regexp determining allowed email origins)
                "additionalWorkflowInput": dict,    (optional, static input always passed to executions)
            }
            Examples:
            {"secretId": "las:secret:<uuid>"}
            {"secretId": "las:secret:<uuid>", "allowedOrigins": [".+@myemaildomain.com"]}
            {"secretId": "las:secret:<uuid>", "allowedOrigins": ["foobar@myemaildomain.com"]}
            {"secretId": "las:secret:<uuid>", "additionalWorkflowInput": {"foo": "bar"}}
        '''),
    )
    create_workflow_parser.add_argument(
        '--error-config',
        type=json_or_json_path,
        help=textwrap.dedent('''
            Path or inline JSON with the error configuration for the workflow
            {
                "manualRetry": boolean,     (optional, failing transitions will become retryable if set to true)
                "email": str                (optional, failing transitions will send an error summary to this email)
            }
            Examples:
            {"manualRetry": true}
            {"manualRetry": true, "email": "foobar@myemaildomain.com"}
        '''),
    )
    create_workflow_parser.add_argument(
        '--completed-config',
        type=json_or_json_path,
        help=textwrap.dedent('''
            Path or inline JSON with the completed configuration for the workflow. The code provided will be run after
            a workflow execution has completed regardless of its final status.
            {
                "imageUrl": str,            (required, docker image URL)
                "secretId": str,            (optional, containing username and password if the docker image is private)
                "environment": dict,        (optional, environment variables passed to the docker container)
                "environmentSecrets": list  (optional, secrets passed to the docker container as environment variables)
            }
            Examples:
            {"imageUrl": "library/repo:tag"}
            {"imageUrl": "library/repo:tag", "secretId": "las:secret:<uuid>"}
            {"imageUrl": "foo/bar:tag", "environment": {"SOME_KEY": "SOME_VALUE"}}
            {"imageUrl": "foo/bar:tag", "environment": {"foo": "bar"}, "environmentSecrets": ["las:secret:<uuid>"]}
        '''),
    )
    create_workflow_parser.add_argument(
        '--metadata',
        type=json_or_json_path,
        help='Add additional custom information about the workflow (JSON or path to JSON file)',
    )
    create_workflow_parser.set_defaults(cmd=create_workflow)

    update_workflow_parser = subparsers.add_parser('update', formatter_class=RawTextHelpFormatter)
    update_workflow_parser.add_argument('workflow_id')
    update_workflow_parser.add_argument('--name', type=nullable(str), default=NotProvided)
    update_workflow_parser.add_argument('--description', type=nullable(str), default=NotProvided)
    update_workflow_parser.add_argument(
        '--email-config',
        default=NotProvided,
        type=nullable(json_or_json_path),
        help=textwrap.dedent('''
            Path or inline JSON with configuration to enable email input to workflow. The required secretId must have
            permissions to call POST /workflows/:id/executions
            {
                "secretId": string,                 (required)
                "allowedOrigins": list[str],        (optional, list of regexp determining allowed email origins)
                "additionalWorkflowInput": dict,    (optional, static input always passed to executions)
            }
            Examples:
            {"secretId": "las:secret:<uuid>"}
            {"secretId": "las:secret:<uuid>", "allowedOrigins": [".+@myemaildomain.com"]}
            {"secretId": "las:secret:<uuid>", "allowedOrigins": ["foobar@myemaildomain.com"]}
            {"secretId": "las:secret:<uuid>", "additionalWorkflowInput": {"foo": "bar"}}
        ''')
    )
    update_workflow_parser.add_argument(
        '--error-config',
        type=json_or_json_path,
        help=textwrap.dedent('''
            Path or inline JSON with the error configuration for the workflow
            {
                "manualRetry": boolean,     (optional, failing transitions will become retryable if set to true)
                "email": str                (optional, failing transitions will send an error summary to this email)
            }
            Examples:
            {"manualRetry": true}
            {"manualRetry": true, "email": "foobar@myemaildomain.com"}
        '''),
    )
    update_workflow_parser.add_argument(
        '--completed-config',
        type=json_or_json_path,
        help=textwrap.dedent('''
            Path or inline JSON with the completed configuration for the workflow. The code provided will be run after
            a workflow execution has completed regardless of its final status.
            {
                "imageUrl": str,            (required, docker image URL)
                "secretId": str,            (optional, containing username and password if the docker image is private)
                "environment": dict,        (optional, environment variables passed to the docker container)
                "environmentSecrets": list  (optional, secrets passed to the docker container as environment variables)
            }
            Examples:
            {"imageUrl": "library/repo:tag"}
            {"imageUrl": "library/repo:tag", "secretId": "las:secret:<uuid>"}
            {"imageUrl": "foo/bar:tag", "environment": {"SOME_KEY": "SOME_VALUE"}}
            {"imageUrl": "foo/bar:tag", "environment": {"foo": "bar"}, "environmentSecrets": ["las:secret:<uuid>"]}
        '''),
    )
    update_workflow_parser.add_argument(
        '--metadata',
        type=json_or_json_path,
        help='Add additional custom information about the workflow (JSON or path to JSON file)',
    )
    update_workflow_parser.add_argument(
        '--status',
        choices={'development', 'production'},
        help='Set status of workflow to development or production',
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
    update_workflow_execution_group = update_workflow_execution_parser.add_mutually_exclusive_group()
    update_workflow_execution_group.add_argument(
        '--next-transition-id',
        help='Specify which transition to continue from. Use las:transition:commons-failed to end an execution',
    )
    update_workflow_execution_group.add_argument(
        '--status',
        choices={'completed', 'succeeded'},
        help='Change status of workflow execution, can only update from succeeded to completed and vice versa',
    )
    update_workflow_execution_parser.set_defaults(cmd=update_workflow_execution)

    delete_workflow_execution_parser = subparsers.add_parser('delete-execution')
    delete_workflow_execution_parser.add_argument('workflow_id')
    delete_workflow_execution_parser.add_argument('execution_id')
    delete_workflow_execution_parser.set_defaults(cmd=delete_workflow_execution)

    create_default_workflow_parser = subparsers.add_parser('create-default')
    create_default_action = create_default_workflow_parser.add_mutually_exclusive_group(required=False)
    create_default_action.add_argument('--from-model-id', help='The model to generate the workflow for')
    create_default_workflow_parser.add_argument('name', help='Name of the workflow')
    create_default_workflow_parser.add_argument('--preprocess-image', default='lucidtechai/preprocess:v2.3.0', help='Docker image for the preprocessor')
    create_default_workflow_parser.add_argument('--postprocess-image', default='lucidtechai/postprocess:v2.2.0', help='Docker image for the postprocessor')
    create_default_workflow_parser.set_defaults(cmd=workflows.create_default_workflow)

    return parser
