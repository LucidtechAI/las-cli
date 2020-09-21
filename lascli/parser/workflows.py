from las import Client
import json
import pathlib


def list_workflows(las_client: Client):
    return las_client.list_workflows()


def create_workflow(las_client: Client, path, name, description, language, version, error_config):
    input_dict = json.loads(pathlib.Path(path).read_text())
    error_config = json.loads(error_config) if error_config else None
    return las_client.create_workflow(input_dict, name, description, language, version, error_config)


def execute_workflow(las_client: Client, workflow_id, path):
    content = json.loads(pathlib.Path(path).read_text())
    return las_client.execute_workflow(workflow_id, content)


def create_workflows_parser(subparsers):
    parser = subparsers.add_parser('workflows')
    subparsers = parser.add_subparsers()

    list_workflows_parser = subparsers.add_parser('list')
    list_workflows_parser.set_defaults(cmd=list_workflows)

    create_workflow_parser = subparsers.add_parser('create')
    create_workflow_parser.add_argument('path')
    create_workflow_parser.add_argument('--name', default='no_name_provided')
    create_workflow_parser.add_argument('--description', default='no description provided')
    create_workflow_parser.add_argument('--language', default='ASL')
    create_workflow_parser.add_argument('--version', default='1.0.0')
    create_workflow_parser.add_argument('--error-config', type=str, default=None)
    create_workflow_parser.set_defaults(cmd=create_workflow)

    execute_workflow_parser = subparsers.add_parser('execute')
    execute_workflow_parser.add_argument('workflow_id')
    execute_workflow_parser.add_argument('path', help='path to json-file with input to the first state of the workflow')
    execute_workflow_parser.set_defaults(cmd=execute_workflow)

    return parser
