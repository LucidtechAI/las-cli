import string
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

