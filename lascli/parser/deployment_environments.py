from las import Client


def list_deployment_environments(las_client: Client, owner, **optional_args):
    return las_client.list_deployment_environments(owner=owner, **optional_args)


def get_deployment_environment(las_client: Client, deployment_environment_id):
    return las_client.get_deployment_environment(deployment_environment_id)


def create_deployment_environments_parser(subparsers):
    parser = subparsers.add_parser('deployment-environments')
    subparsers = parser.add_subparsers()

    list_deployment_environments_parser = subparsers.add_parser('list')
    list_deployment_environments_parser.add_argument(
        '--owner', '-o',
        nargs='+',
        help='Organizations whose deployment_environments to list',
    )
    list_deployment_environments_parser.add_argument('--max-results', '-m', type=int, default=None)
    list_deployment_environments_parser.add_argument('--next-token', '-n', type=str, default=None)
    list_deployment_environments_parser.set_defaults(cmd=list_deployment_environments)

    get_deployment_environment_parser = subparsers.add_parser('get')
    get_deployment_environment_parser.add_argument('deployment_environment_id')
    get_deployment_environment_parser.set_defaults(cmd=get_deployment_environment)

    return parser
