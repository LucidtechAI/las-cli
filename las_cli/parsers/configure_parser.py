from configparser import ConfigParser
from os import makedirs


def configure(args):
    profile = input('Name of profile (Enter for default): ')
    api_key = input('Your API key: ')
    stage = input('API stage name (Enter for default): ')
    base_endpoint = input('API base endpoint name (Enter for default): ')

    makedirs(args.config_dir, exist_ok=True)
    profile = profile or 'default'
    stage = stage or 'v0'
    base_endpoint = base_endpoint or 'https://api.lucidtech.ai'

    config = ConfigParser()
    config.read(args.config_path)
    config[profile] = {
        'api_key': api_key,
        'stage': stage,
        'base_endpoint': base_endpoint
    }

    with open(args.config_path, 'w') as fp:
        config.write(fp)


def configure_parser(subparsers):
    parser = subparsers.add_parser('configure', help='Configure las-cli')
    parser.set_defaults(cmd=configure)
