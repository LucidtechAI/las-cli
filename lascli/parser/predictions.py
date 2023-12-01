import json
import textwrap
from argparse import RawTextHelpFormatter

from las import Client

from lascli.util import json_or_json_path


def create_prediction(las_client: Client, document_id, model_id, **optional_args):
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
    create_predicton_parser.add_argument('--preprocess-config', type=json_or_json_path, help=textwrap.dedent('''
        Path or inline JSON with the pre processing configuration for this prediction
        {
            "autoRotate": True | False                          (optional)
            "maxPages": 1 - 3                                   (optional)
            "imageQuality": "LOW" | "HIGH"                      (optional)
            "pages": List with up to 3 page-indices to process  (optional)
            "rotation": 0, 90, 180 or 270                       (optional)
        }
        Examples:
        {"pages": [0, 1, 5], "autoRotate": True}
        {"pages": [0, 1, -1], "rotation": 90, "imageQuality": "HIGH"}
        {"maxPages": 3, "imageQuality": "LOW"}
    '''))
    create_predicton_parser.add_argument('--postprocess-config', type=json_or_json_path, help=textwrap.dedent('''
        Path or inline JSON with the post processing configuration for this prediction
        {
            "strategy": "BEST_FIRST" | "BEST_N_PAGES",  (required)
            "parameters": {                             (required if strategy=BEST_N_PAGES, omit otherwise)
                "n": int,                               (required if strategy=BEST_N_PAGES, omit otherwise)
                "collapse": true | false (default)      (optional if strategy=BEST_N_PAGES, omit otherwise)
            }
        }
        Examples:
        {"strategy": "BEST_FIRST", "outputFormat": "v2"}
        {"strategy": "BEST_N_PAGES", "parameters": {"n": 3}}
        {"strategy": "BEST_N_PAGES", "parameters": {"n": 3, "collapse": true}}
    '''))
    create_predicton_parser.set_defaults(cmd=create_prediction)

    list_predictions_parser = subparsers.add_parser('list')
    list_predictions_parser.add_argument('--max-results', '-m', type=int, default=None)
    list_predictions_parser.add_argument('--next-token', '-n', default=None)
    list_predictions_parser.add_argument('--sort-by', choices={'createdTime'})
    list_predictions_parser.add_argument('--order', choices={'ascending', 'descending'})
    list_predictions_parser.add_argument('--model-id')
    list_predictions_parser.set_defaults(cmd=list_predictions)

    return parser
