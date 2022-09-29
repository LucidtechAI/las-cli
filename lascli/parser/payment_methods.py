from las import Client

from lascli.util import nullable, NotProvided


def create_payment_method(las_client: Client, **optional_args):
    return las_client.create_payment_method(**optional_args)


def get_payment_method(las_client: Client, payment_method_id):
    return las_client.get_payment_method(payment_method_id)


def list_payment_methods(las_client: Client, max_results=None, next_token=None):
    return las_client.list_payment_methods(max_results=max_results, next_token=next_token)


def update_payment_method(las_client: Client, payment_method_id, stripe_setup_intent_secret, **optional_args):
    return las_client.update_payment_method(
        payment_method_id,
        stripe_setup_intent_secret=stripe_setup_intent_secret,
        **optional_args,
    )


def delete_payment_method(las_client: Client, payment_method_id):
    return las_client.delete_payment_method(payment_method_id)


def create_payment_methods_parser(subparsers):
    parser = subparsers.add_parser('payment-methods')
    subparsers = parser.add_subparsers()

    create_payment_method_parser = subparsers.add_parser('create')
    create_payment_method_parser.add_argument('--description')
    create_payment_method_parser.add_argument('--name')
    create_payment_method_parser.set_defaults(cmd=create_payment_method)

    get_payment_method_parser = subparsers.add_parser('get')
    get_payment_method_parser.add_argument('payment_method_id')
    get_payment_method_parser.set_defaults(cmd=get_payment_method)

    list_payment_methods_parser = subparsers.add_parser('list')
    list_payment_methods_parser.add_argument('--max-results', '-m', type=int, default=None)
    list_payment_methods_parser.add_argument('--next-token', '-n', default=None)
    list_payment_methods_parser.set_defaults(cmd=list_payment_methods)

    update_payment_method_parser = subparsers.add_parser('update')
    update_payment_method_parser.add_argument('payment_method_id')
    update_payment_method_parser.add_argument(
        '--stripe-setup-intent-secret',
        help='Add this parameter to complete payment method setup',
    )
    update_payment_method_parser.add_argument('--name', type=nullable(str), default=NotProvided)
    update_payment_method_parser.add_argument('--description', type=nullable(str), default=NotProvided)
    update_payment_method_parser.set_defaults(cmd=update_payment_method)

    delete_payment_method_parser = subparsers.add_parser('delete')
    delete_payment_method_parser.add_argument('payment_method_id')
    delete_payment_method_parser.set_defaults(cmd=delete_payment_method)

    return parser
