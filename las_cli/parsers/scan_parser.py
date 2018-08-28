import json

from configparser import ConfigParser
from functools import partial
from las import Client, Receipt, Invoice


class MissingFileOrUrlException(Exception):
    pass


class InvalidDocumentTypeException(Exception):
    pass


def get_kwargs(args):
    kwargs = {
        'minConfidence': args.min_confidence,
        'customModel': args.custom_model
    }

    return {k: v for k, v in kwargs.items() if v}


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
        else:
            raise MissingFileOrUrlException('Need to specify url or filename')
        response = client.scan_receipt(receipt, **get_kwargs(args))
    elif args.document_type == 'invoice':
        if args.filename:
            invoice = Invoice(filename=args.filename)
        elif args.url:
            invoice = Invoice(url=args.url)
        else:
            raise MissingFileOrUrlException('Need to specify url or filename')
        response = client.scan_invoice(invoice, **get_kwargs(args))
    else:
        raise InvalidDocumentTypeException()

    if response.status_code == 200:
        print(json.dumps(response.detections, indent=2))
    else:
        print(response.requests_response)


def scan_parser(subparsers):
    parser = subparsers.add_parser('scan', help='Scan receipt image')
    parser.add_argument('document_type', choices={'receipt', 'invoice'})
    parser.add_argument('--filename', help='Filename of receipt/invoice image')
    parser.add_argument('--url', help='Url of receipt/invoice image')
    parser.add_argument('--min_confidence', help='Minimum confidence of scan', type=float)
    parser.add_argument('--custom_model', help='Optional specify a custom model name')
    parser.add_argument('--profile', default='default',
                        help='Choose profile (~/.lucidtech/las-cli.cfg')
    parser.set_defaults(cmd=scan)
