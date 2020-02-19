from las import Client


def delete_consent(las_client: Client, consent_id):
    return las_client.delete_consent(consent_id)


def create_consents_parser(subparsers):
    parser = subparsers.add_parser('consents')
    subparsers = parser.add_subparsers()

    delete_consent_parser = subparsers.add_parser('delete')
    delete_consent_parser.add_argument('consent_id')
    delete_consent_parser.set_defaults(cmd=delete_consent)

    return parser
