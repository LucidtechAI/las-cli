from configparser import ConfigParser
from functools import partial
from las import Client, Receipt


def scan(args):
    config = ConfigParser()
    config.read(args.config_path)
    cfg = partial(config.get, args.profile, fallback=None)

    client = Client(cfg('api_key'), cfg('base_endpoint'), cfg('stage'))

    if args.filename:
        receipt = Receipt(filename=args.filename)
    elif args.url:
        receipt = Receipt(url=args.url)

    print(client.scan_receipt(receipt))


def scan_parser(subparsers):
    parser = subparsers.add_parser('scan', help='Scan receipt image')
    parser.add_argument('--filename', help='Filename of receipt image')
    parser.add_argument('--url', help='Url of receipt image')
    parser.add_argument('--profile', default='default',
                        help='Choose profile (~/.lucidtech/las-cli.cfg')
    parser.set_defaults(cmd=scan)
