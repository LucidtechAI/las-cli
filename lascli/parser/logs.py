from las import Client


def get_log(las_client: Client, log_id):
    return las_client.get_log(log_id)


def create_logs_parser(subparsers):
    parser = subparsers.add_parser('logs')
    subparsers = parser.add_subparsers()

    get_log_parser = subparsers.add_parser('get')
    get_log_parser.add_argument('log_id')
    get_log_parser.set_defaults(cmd=get_log)

    return parser
