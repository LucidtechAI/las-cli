import json

from configparser import ConfigParser
from functools import partial
from las import Client, Receipt, Invoice


def scan(args):
    config = ConfigParser()
    config.read(args.config_path)
    cfg = partial(config.get, args.profile, fallback=None)

    client = Client(cfg('api_key'), cfg('base_endpoint'), cfg('stage'))

    if args.document_type == 'receipt':
        if args.filename:
            receipt = Receipt(filename=args.filename)
        elif args.url:
            receipt = Receipt(url=args.url)

        print(json.dumps(client.scan_receipt(receipt), indent=2))
    elif args.document_type == 'invoice':
        if args.filename:
            invoice = Invoice(filename=args.filename)
        elif args.url:
            invoice = Invoice(url=args.url)

        print(json.dumps(client.scan_invoice(invoice), indent=2))


def scan_parser(subparsers):
    parser = subparsers.add_parser('scan', help='Scan receipt image')
    parser.add_argument('document_type', choices={'receipt', 'invoice'})
    parser.add_argument('--filename', help='Filename of receipt/invoice image')
    parser.add_argument('--url', help='Url of receipt/invoice image')
    parser.add_argument('--profile', default='default',
                        help='Choose profile (~/.lucidtech/las-cli.cfg')
    parser.set_defaults(cmd=scan)
