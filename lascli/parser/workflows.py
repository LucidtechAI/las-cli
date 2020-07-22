from las import Client
import json
import pathlib


def list_workflows(las_client: Client):
    return las_client.list_workflows()


def create_workflow(las_client: Client, path, name, description, type, version):
    content = json.loads(pathlib.Path(path).read_text())
    return las_client.create_workflow(content, name, description, type, version)


def create_workflows_parser(subparsers):
    parser = subparsers.add_parser('workflows')
    subparsers = parser.add_subparsers()

    list_workflows_parser = subparsers.add_parser('list')
    list_workflows_parser.set_defaults(cmd=list_workflows)

    create_workflow_parser = subparsers.add_parser('create')
    create_workflow_parser.add_argument('path')
    create_workflow_parser.add_argument('--name', default='no name provided')
    create_workflow_parser.add_argument('--description', default='no description provided')
    create_workflow_parser.add_argument('--type', default='ASL')
    create_workflow_parser.add_argument('--version', default='1.0')
    create_workflow_parser.set_defaults(cmd=create_workflow)

    return parser
