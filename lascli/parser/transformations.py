from las import Client
import json
import pathlib


def create_transformation(las_client: Client, transformation_type, in_schema_path, out_schema_path, params_path):
    in_schema = json.loads(pathlib.Path(in_schema_path).read_text())
    out_schema = json.loads(pathlib.Path(out_schema_path).read_text())
    params = json.loads(pathlib.Path(params_path).read_text())
    return las_client.create_transformation(transformation_type, in_schema, out_schema, params)


def execute_transformation(las_client: Client, transformation_id, path):
    content = json.loads(pathlib.Path(path).read_text())
    return las_client.execute_transformation(transformation_id, content)


def create_transformations_parser(subparsers):
    parser = subparsers.add_parser('transformations')
    subparsers = parser.add_subparsers()

    create_transformation_parser = subparsers.add_parser('create')
    create_transformation_parser.add_argument('transformation_type', help='either "docker" or "manual"')
    create_transformation_parser.add_argument('in_schema_path')
    create_transformation_parser.add_argument('out_schema_path')
    create_transformation_parser.add_argument('params_path')
    create_transformation_parser.set_defaults(cmd=create_transformation)

    execute_transformation_parser = subparsers.add_parser('execute')
    execute_transformation_parser.add_argument('transformation_id')
    execute_transformation_parser.add_argument('path', help='path to json-file with input to the first state of the transformation')
    execute_transformation_parser.set_defaults(cmd=execute_transformation)

    return parser
