import json
import pathlib

from las import Client

from lascli.util import nullable, NotProvided


def list_workflows(las_client: Client, max_results=None, next_token=None):
    return las_client.list_workflows(max_results=max_results, next_token=next_token)


def create_workflow(las_client: Client, specification_path, error_config, **optional_args):
    specification = json.loads(pathlib.Path(specification_path).read_text())
    error_config = json.loads(error_config) if error_config else None
    return las_client.create_workflow(specification, error_config=error_config, **optional_args)


def get_workflow(las_client: Client, workflow_id):
    return las_client.get_workflow(workflow_id)


def update_workflow(las_client: Client, workflow_id, **optional_args):
    return las_client.update_workflow(workflow_id, **optional_args)


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
        next_token=next_token,
    )


def delete_workflow(las_client: Client, workflow_id):
    return las_client.delete_workflow(workflow_id)


def delete_workflow_execution(las_client: Client, workflow_id, execution_id):
    return las_client.delete_workflow_execution(workflow_id, execution_id)


def create_workflows_parser(subparsers):
    parser = subparsers.add_parser('workflows')
    subparsers = parser.add_subparsers()

    list_workflows_parser = subparsers.add_parser('list')
    list_workflows_parser.add_argument('--max-results', '-m', type=int)
    list_workflows_parser.add_argument('--next-token', '-n', type=str)
    list_workflows_parser.set_defaults(cmd=list_workflows)

    create_workflow_parser = subparsers.add_parser('create')
    create_workflow_parser.add_argument('specification_path')
    create_workflow_parser.add_argument('--name')
    create_workflow_parser.add_argument('--description')
    create_workflow_parser.add_argument('--error-config', type=str)
    create_workflow_parser.set_defaults(cmd=create_workflow)

    update_workflow_parser = subparsers.add_parser('update')
    update_workflow_parser.add_argument('workflow_id')
    update_workflow_parser.add_argument('--name', type=nullable, default=NotProvided)
    update_workflow_parser.add_argument('--description', type=nullable, default=NotProvided)
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
    list_executions_parser.set_defaults(cmd=list_workflow_executions)

    get_workflow_parser = subparsers.add_parser('get')
    get_workflow_parser.add_argument('workflow_id')
    get_workflow_parser.set_defaults(cmd=get_workflow)

    delete_workflow_parser = subparsers.add_parser('delete')
    delete_workflow_parser.add_argument('workflow_id')
    delete_workflow_parser.set_defaults(cmd=delete_workflow)

    delete_workflow_execution_parser = subparsers.add_parser('delete-execution')
    delete_workflow_execution_parser.add_argument('workflow_id')
    delete_workflow_execution_parser.add_argument('execution_id')
    delete_workflow_execution_parser.set_defaults(cmd=delete_workflow_execution)

    return parser
