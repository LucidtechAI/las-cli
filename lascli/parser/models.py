import json
from pathlib import Path

from las import Client

from lascli.util import NotProvided, nullable


def create_model(
    las_client: Client,
    width,
    height,
    field_config_path,
    preprocess_config_path=None,
    **optional_args,
):
    field_config = json.loads(Path(field_config_path).read_text())
    preprocess_config = json.loads(Path(preprocess_config_path).read_text()) if preprocess_config_path else None
    return las_client.create_model(
        width=width,
        height=height,
        field_config=field_config,
        preprocess_config=preprocess_config,
        **optional_args
    )


def list_models(las_client: Client, max_results, next_token):
    return las_client.list_models(max_results=max_results, next_token=next_token)


def update_model(
    las_client: Client,
    model_id,
    width=None,
    height=None,
    field_config_path=None,
    preprocess_config_path=None,
    start_training=False,
    **optional_args,
):
    field_config = json.loads(Path(field_config_path).read_text()) if field_config_path else None
    preprocess_config = json.loads(Path(preprocess_config_path).read_text()) if preprocess_config_path else None
    status = 'training' if start_training else None

    return las_client.update_model(
        model_id=model_id,
        width=width,
        height=height,
        field_config=field_config,
        preprocess_config=preprocess_config,
        status=status,
        **optional_args,
    )


def create_models_parser(subparsers):
    parser = subparsers.add_parser('models')
    subparsers = parser.add_subparsers()

    create_parser = subparsers.add_parser('create')
    create_parser.add_argument('width', type=int)
    create_parser.add_argument('height', type=int)
    create_parser.add_argument('field_config_path', help='configuration of the fields that the model will predict')
    create_parser.add_argument('--preprocess-config-path', '-p', help='configuration of the step before the prediction')
    create_parser.add_argument('--name')
    create_parser.add_argument('--description')
    create_parser.set_defaults(cmd=create_model)

    update_parser = subparsers.add_parser('update')
    update_parser.add_argument('model_id')
    update_parser.add_argument(
        '--field-config-path',
        '-f',
        help='configuration of the fields that the model will predict',
    )
    update_parser.add_argument('--width', type=int)
    update_parser.add_argument('--height', type=int)
    update_parser.add_argument('--start-training', action='store_true', default=False)
    update_parser.add_argument('--preprocess-config-path', '-p', help='configuration of the step before the prediction')
    update_parser.add_argument('--name', type=nullable, default=NotProvided)
    update_parser.add_argument('--description', type=nullable, default=NotProvided)
    update_parser.set_defaults(cmd=update_model)

    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('--max-results', '-m', type=int, default=None)
    list_parser.add_argument('--next-token', '-n', type=str, default=None)
    list_parser.set_defaults(cmd=list_models)

    return parser
