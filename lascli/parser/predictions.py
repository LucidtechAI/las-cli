from las import Client


def post_predictions(las_client: Client, document_id, model_id):
    return las_client.create_prediction(document_id, model_id)


def list_predictions(las_client: Client, max_results=None, next_token=None):
    return las_client.list_predictions(max_results=max_results, next_token=next_token)


def create_predictions_parser(subparsers):
    parser = subparsers.add_parser('predictions')
    subparsers = parser.add_subparsers()

    create_predicton_parser = subparsers.add_parser('create')
    create_predicton_parser.add_argument('document_id')
    create_predicton_parser.add_argument('model_id')
    create_predicton_parser.set_defaults(cmd=post_predictions)

    list_predictions_parser = subparsers.add_parser('list')
    list_predictions_parser.add_argument('--max-results', '-m', type=int, default=None)
    list_predictions_parser.add_argument('--next-token', '-n', default=None)
    list_predictions_parser.set_defaults(cmd=list_predictions)

    return parser
