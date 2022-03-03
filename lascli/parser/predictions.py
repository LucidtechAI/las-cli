import json
import textwrap
from argparse import RawTextHelpFormatter

from las import Client


def post_predictions(las_client: Client, document_id, model_id, **optional_args):
    return las_client.create_prediction(document_id, model_id, **optional_args)


def list_predictions(las_client: Client, **optional_args):
    return las_client.list_predictions(**optional_args)


def create_predictions_parser(subparsers):
    parser = subparsers.add_parser('predictions')
    subparsers = parser.add_subparsers()

    create_predicton_parser = subparsers.add_parser('create', formatter_class=RawTextHelpFormatter)
    create_predicton_parser.add_argument('document_id')
    create_predicton_parser.add_argument('model_id', help='Id of model to use for predictions')
    create_predicton_parser.add_argument('--training-id', help='Id of training to use for predictions')
    create_predicton_parser.add_argument('--auto-rotate', action='store_true', default=False)
    create_predicton_parser.add_argument('--max-pages', type=int, default=1)
    create_predicton_parser.add_argument('--image-quality', type=str, default='LOW', choices={'LOW', 'HIGH'})
    create_predicton_parser.add_argument('--postprocess-config', type=json.loads, help=textwrap.dedent('''
        Post processing configuration for predictions
        {
            "strategy": "BEST_FIRST" | "BEST_N_PAGES",  (required)
            "parameters": {                             (required if strategy=BEST_N_PAGES, omit otherwise)
                "n": int,                               (required if strategy=BEST_N_PAGES, omit otherwise)
                "collapse": true | false (default)      (optional if strategy=BEST_N_PAGES, omit otherwise)
            }
        }
        Examples:
        {"strategy": "BEST_FIRST"}
        {"strategy": "BEST_N_PAGES", "parameters": {"n": 3}}
        {"strategy": "BEST_N_PAGES", "parameters": {"n": 3, "collapse": true}}
    '''))
    create_predicton_parser.set_defaults(cmd=post_predictions)

    list_predictions_parser = subparsers.add_parser('list')
    list_predictions_parser.add_argument('--max-results', '-m', type=int, default=None)
    list_predictions_parser.add_argument('--next-token', '-n', default=None)
    list_predictions_parser.set_defaults(cmd=list_predictions)

    return parser
