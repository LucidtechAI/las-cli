from las import Client
import json
import pathlib


def create_transition(las_client: Client, transition_type, in_schema_path, out_schema_path, params_path):
    in_schema = json.loads(pathlib.Path(in_schema_path).read_text())
    out_schema = json.loads(pathlib.Path(out_schema_path).read_text())
    params = json.loads(pathlib.Path(params_path).read_text()) if params_path else None
    return las_client.create_transition(transition_type, in_schema, out_schema, params)


def execute_transition(las_client: Client, transition_id):
    return las_client.execute_transition(transition_id)


def update_transition_execution(las_client: Client, transition_id, execution_id, status, error_path, output_path):
    output_dict = json.loads(pathlib.Path(output_path).read_text()) if output_path else None
    error_dict = json.loads(pathlib.Path(error_path).read_text()) if error_path else None
    return las_client.update_transition_execution(transition_id, execution_id, status, output_dict, error_dict)


def create_transitions_parser(subparsers):
    parser = subparsers.add_parser('transitions')
    subparsers = parser.add_subparsers()

    create_parser = subparsers.add_parser('create')
    create_parser.add_argument('transition_type', choices=["docker", "manual"])
    create_parser.add_argument('in_schema_path')
    create_parser.add_argument('out_schema_path')
    create_parser.add_argument('params_path', default=None, nargs='?', help='parameters to the docker image')
    create_parser.set_defaults(cmd=create_transition)

    execute_parser = subparsers.add_parser('execute')
    execute_parser.add_argument('transition_id')
    execute_parser.set_defaults(cmd=execute_transition)

    update_parser = subparsers.add_parser('update')
    update_parser.add_argument('transition_id')
    update_parser.add_argument('execution_id')
    update_parser.add_argument('status', choices=['succeeded', 'failed'])
    update_parser.add_argument('--output_path', '-o', default=None)
    update_parser.add_argument('--error_path', '-e', default=None)
    update_parser.set_defaults(cmd=update_transition_execution)

    return parser
