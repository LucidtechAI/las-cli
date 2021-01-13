from datetime import datetime
from las import Client


def parse_log(response):
    log_events = []
    for event in response['events']:
        timestamp = event['timestamp']
        message = event['message']
        log_events.append(f'{datetime.fromtimestamp(timestamp)}: {message}')
    return '\n'.join(log_events)


def get_log(las_client: Client, log_id, pretty):
    response = las_client.get_log(log_id)
    if pretty:
        response = parse_log(response)
    return response


def create_logs_parser(subparsers):
    parser = subparsers.add_parser('logs')
    subparsers = parser.add_subparsers()

    get_log_parser = subparsers.add_parser('get')
    get_log_parser.add_argument('log_id')
    get_log_parser.add_argument('--pretty', action='store_true', help='Parse output to make it more readable')
    get_log_parser.set_defaults(cmd=get_log)

    return parser
