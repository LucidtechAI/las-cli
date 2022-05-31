import csv
import json
import pathlib
import string
import tempfile
from os import urandom

from random import choice, randint
from las import Client
from requests_mock import Mocker
import pytest

from lascli.__main__ import create_parser
from . import util


@pytest.fixture(scope='session')
def token():
    return {
        'access_token': ''.join(choice(string.ascii_uppercase) for _ in range(randint(50, 50))),
        'expires_in': 123456789,
    }


@pytest.fixture(scope='session', autouse=True)
def mock_access_token_endpoint(token):
    with Mocker(real_http=True) as m:
        m.post('/token', json=token)
        yield


@pytest.fixture(scope='session')
def parser():
    return create_parser()


@pytest.fixture(scope='module')
def client():
    client = Client()
    return client


@pytest.fixture
def mime_type():
    return 'image/jpeg'


@pytest.fixture(scope='function')
def content():
    """
    Yields a random JPEG bytestring with a length 2E4
    """
    yield b'\xFF\xD8\xFF\xEE' + urandom(int(2E4))


@pytest.fixture(params=util.name_and_description())
def name_and_description(request):
    return request.param


@pytest.fixture(params=util.max_results_and_next_token())
def list_defaults(request):
    return request.param


@pytest.fixture(params=[(), ('--metadata', str(util.metadata_path()))])
def metadata(request):
    return request.param


def _documents_iter(tmp_dir_path):
    for i in range(0, 5):
        pdf_path = tmp_dir_path / f'{i}.pdf'
        pdf_path.write_bytes(util.create_pdf())
        yield i, pdf_path

    for i in range(5, 10):
        jpeg_path = tmp_dir_path / f'{i}.jpeg'
        jpeg_path.write_bytes(util.create_jpeg())
        yield i, jpeg_path


def documents_dir():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir_path = pathlib.Path(tmp_dir)

        for i, document in _documents_iter(tmp_dir_path):
            json_path = tmp_dir_path / f'{i}.json'
            json_path.write_text(json.dumps(util.create_ground_truth()))

        yield tmp_dir


def json_and_documents_dir():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir_path = pathlib.Path(tmp_dir)
        json_data = {}

        for _, document in _documents_iter(tmp_dir_path):
            json_data[str(document)] = util.create_ground_truth()

        json_file_path = tmp_dir_path / 'data.json'
        json_file_path.write_text(json.dumps(json_data))
        
        yield str(json_file_path)
        

def csv_and_documents_dir():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir_path = pathlib.Path(tmp_dir)
        csv_file_path = tmp_dir_path / 'data.csv'

        with csv_file_path.open('w') as csvfile:
            field_names = ['Document_name', 'total', 'date']
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()

            for _, document in _documents_iter(tmp_dir_path):
                fields = {gt['label']: gt['value'] for gt in util.create_ground_truth()}
                writer.writerow({'Document_name': str(document), **fields})
                
        yield str(csv_file_path)


@pytest.fixture(params=[documents_dir, json_and_documents_dir, csv_and_documents_dir])
def create_documents_input(request):
    yield from request.param()
