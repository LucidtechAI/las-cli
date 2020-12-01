from las import Client
import json
import pathlib


def list_workflows(las_client: Client, max_results, next_token):
    return las_client.list_workflows(max_results=max_results, next_token=next_token)


def create_workflow(las_client: Client, specification_path, name, description, error_config):
    specification = json.loads(pathlib.Path(specification_path).read_text())
    error_config = json.loads(error_config) if error_config else None
    return las_client.create_workflow(specification, name, description, error_config)


def update_workflow(las_client: Client, workflow_id, name, description):
    return las_client.update_workflow(
        workflow_id,
        name=name,
        description=description,
    )


def execute_workflow(las_client: Client, workflow_id, path):
    content = json.loads(pathlib.Path(path).read_text())
    return las_client.execute_workflow(workflow_id, content)


def list_workflow_executions(las_client: Client, workflow_id, status, order, sort_by, max_results, next_token):
    return las_client.list_workflow_executions(
        workflow_id,
        status=status,
        order=order,
        sort_by=sort_by,
        max_results=max_results,
        next_token=next_token)


def delete_workflow(las_client: Client, workflow_id):
    return las_client.delete_workflow(workflow_id)


def create_workflows_parser(subparsers):
    parser = subparsers.add_parser('workflows')
    subparsers = parser.add_subparsers()

    list_workflows_parser = subparsers.add_parser('list')
    list_workflows_parser.add_argument('--max-results', '-m', type=int)
    list_workflows_parser.add_argument('--next-token', '-n', type=str)
    list_workflows_parser.set_defaults(cmd=list_workflows)

    create_workflow_parser = subparsers.add_parser('create')
    create_workflow_parser.add_argument('specification_path')
    create_workflow_parser.add_argument('name')
    create_workflow_parser.add_argument('--description')
    create_workflow_parser.add_argument('--error-config', type=str)
    create_workflow_parser.set_defaults(cmd=create_workflow)

    update_workflow_parser = subparsers.add_parser('update')
    update_workflow_parser.add_argument('workflow_id')
    update_workflow_parser.add_argument('--name')
    update_workflow_parser.add_argument('--description')
    update_workflow_parser.set_defaults(cmd=update_workflow)

    execute_workflow_parser = subparsers.add_parser('execute')
    execute_workflow_parser.add_argument('workflow_id')
    execute_workflow_parser.add_argument('path', help='path to json-file with input to the first state of the workflow')
    execute_workflow_parser.set_defaults(cmd=execute_workflow)

    list_executions_parser = subparsers.add_parser('list-executions')
    list_executions_parser.add_argument('workflow_id')
    list_executions_parser.add_argument('--status', '-s', nargs='+', help='Only return those with the given status')
    list_executions_parser.add_argument('--max-results', '-m', type=int)
    list_executions_parser.add_argument('--next-token', '-n', type=str)
    list_executions_parser.set_defaults(cmd=list_workflow_executions)

    delete_workflow_parser = subparsers.add_parser('delete')
    delete_workflow_parser.add_argument('workflow_id')
    delete_workflow_parser.set_defaults(cmd=delete_workflow)

    return parser
