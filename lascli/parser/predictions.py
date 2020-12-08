from las import Client


def post_predictions(las_client: Client, document_id, model_id):
    return las_client.create_prediction(document_id, model_id)


def create_predictions_parser(subparsers):
    parser = subparsers.add_parser('predictions')
    subparsers = parser.add_subparsers()

    create_predicton_parser = subparsers.add_parser('create')
    create_predicton_parser.add_argument('document_id')
    create_predicton_parser.add_argument('model_id')
    create_predicton_parser.set_defaults(cmd=post_predictions)

    return parser
