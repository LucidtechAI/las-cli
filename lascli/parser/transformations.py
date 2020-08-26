from las import Client
import json
import pathlib


def create_transformation(las_client: Client, transformation_type, in_schema_path, out_schema_path, params_path):
    in_schema = json.loads(pathlib.Path(in_schema_path).read_text())
    out_schema = json.loads(pathlib.Path(out_schema_path).read_text())
    params = json.loads(pathlib.Path(params_path).read_text()) if params_path else None
    return las_client.create_transformation(transformation_type, in_schema, out_schema, params)


def execute_transformation(las_client: Client, transformation_id, path):
    content = json.loads(pathlib.Path(path).read_text())
    return las_client.execute_transformation(transformation_id, content)


def update_transformation_execution(las_client: Client, transformation_id, execution_id, output):
    return las_client.update_transformation_execution(transformation_id, execution_id, output)


def create_transformations_parser(subparsers):
    parser = subparsers.add_parser('transformations')
    subparsers = parser.add_subparsers()

    create_parser = subparsers.add_parser('create')
    create_parser.add_argument('transformation_type', help='either "docker" or "manual"')
    create_parser.add_argument('in_schema_path')
    create_parser.add_argument('out_schema_path')
    create_parser.add_argument('params_path', default=None, nargs='?')
    create_parser.set_defaults(cmd=create_transformation)

    execute_parser = subparsers.add_parser('execute')
    execute_parser.add_argument('transformation_id')
    execute_parser.add_argument('path', help='path to json-file with input to the first state of the transformation')
    execute_parser.set_defaults(cmd=execute_transformation)

    update_parser = subparsers.add_parser('update')
    update_parser.add_argument('transformation_id')
    update_parser.add_argument('execution_id')
    update_parser.add_argument('output')
    update_parser.set_defaults(cmd=update_transformation_execution)

    return parser
