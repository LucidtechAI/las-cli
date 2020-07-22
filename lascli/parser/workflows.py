from las import Client


def list_workflows(las_client: Client):
    return las_client.list_workflows()


def create_workflows_parser(subparsers):
    parser = subparsers.add_parser('workflows')
    subparsers = parser.add_subparsers()

    list_workflows_parser = subparsers.add_parser('list')
    list_workflows_parser.set_defaults(cmd=list_workflows)

    return parser
