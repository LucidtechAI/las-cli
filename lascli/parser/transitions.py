from las import Client
import json
import pathlib


def create_transition(
    las_client: Client,
    name,
    transition_type,
    in_schema_path,
    out_schema_path,
    params_path,
    description,
):
    in_schema = json.loads(pathlib.Path(in_schema_path).read_text())
    out_schema = json.loads(pathlib.Path(out_schema_path).read_text())
    params = json.loads(pathlib.Path(params_path).read_text()) if params_path else None
    return las_client.create_transition(
        name,
        transition_type,
        in_schema,
        out_schema,
        params=params,
        description=description,
    )


def update_transition(las_client: Client, transition_id, name, in_schema_path, out_schema_path, description):
    in_schema = json.loads(pathlib.Path(in_schema_path).read_text()) if in_schema_path else None
    out_schema = json.loads(pathlib.Path(out_schema_path).read_text()) if out_schema_path else None
    return las_client.update_transition(
        transition_id,
        name=name,
        in_schema=in_schema,
        out_schema=out_schema,
        description=description,
    )


def list_transitions(las_client: Client, transition_type, max_results, next_token):
    return las_client.list_transitions(transition_type=transition_type, max_results=max_results, next_token=next_token)


def execute_transition(las_client: Client, transition_id):
    return las_client.execute_transition(transition_id)


def list_transition_executions(las_client: Client, transition_id, execution_id, status, max_results, next_token):
    return las_client.list_transition_executions(
        transition_id,
        execution_id=execution_id,
        status=status,
        max_results=max_results,
        next_token=next_token,
    )


def update_transition_execution(las_client: Client, transition_id, execution_id, status, error_path, output_path):
    output_dict = json.loads(pathlib.Path(output_path).read_text()) if output_path else None
    error_dict = json.loads(pathlib.Path(error_path).read_text()) if error_path else None
    return las_client.update_transition_execution(
        transition_id,
        execution_id,
        status,
        output=output_dict,
        error=error_dict,
    )


def create_transitions_parser(subparsers):
    parser = subparsers.add_parser('transitions')
    subparsers = parser.add_subparsers()

    create_parser = subparsers.add_parser('create')
    create_parser.add_argument('name')
    create_parser.add_argument('transition_type', choices=["docker", "manual"])
    create_parser.add_argument('in_schema_path')
    create_parser.add_argument('out_schema_path')
    create_parser.add_argument('params_path', nargs='?', help='parameters to the docker image')
    create_parser.add_argument('--description')
    create_parser.set_defaults(cmd=create_transition)

    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('--transition-type', '-t', nargs='+')
    list_parser.add_argument('--max-results', '-m', type=int)
    list_parser.add_argument('--next-token', '-n', type=str)
    list_parser.set_defaults(cmd=list_transitions)

    update_parser = subparsers.add_parser('update')
    update_parser.add_argument('transition_id')
    update_parser.add_argument('--name')
    update_parser.add_argument('--in-schema-path')
    update_parser.add_argument('--out-schema-path')
    update_parser.add_argument('--description')
    update_parser.set_defaults(cmd=update_transition)

    execute_parser = subparsers.add_parser('execute')
    execute_parser.add_argument('transition_id')
    execute_parser.set_defaults(cmd=execute_transition)

    list_executions_parser = subparsers.add_parser('list-executions')
    list_executions_parser.add_argument('transition_id')
    list_executions_parser.add_argument('--execution-id', nargs='+', help='Perform a batch-get on the ids')
    list_executions_parser.add_argument('--status', '-s', nargs='+', help='Only return those with the given status')
    list_executions_parser.add_argument('--max-results', '-m', type=int)
    list_executions_parser.add_argument('--next-token', '-n', type=str)
    list_executions_parser.set_defaults(cmd=list_transition_executions)

    update_execution_parser = subparsers.add_parser('update-execution')
    update_execution_parser.add_argument('transition_id')
    update_execution_parser.add_argument('execution_id')
    update_execution_parser.add_argument('status', choices=['succeeded', 'failed', 'rejected', 'retry'])
    update_execution_parser.add_argument('--output_path', '-o')
    update_execution_parser.add_argument('--error_path', '-e')
    update_execution_parser.set_defaults(cmd=update_transition_execution)

    return parser
