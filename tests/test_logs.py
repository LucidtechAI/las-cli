import pytest
from tests import service, util


@pytest.mark.parametrize('w_id', service.optional_resource_id('workflow'))
@pytest.mark.parametrize('t_id', service.optional_resource_id('workflow'))
@pytest.mark.parametrize('we_id', service.optional_resource_id('workflow-execution'))
@pytest.mark.parametrize('te_id', service.optional_resource_id('workflow-execution'))
@pytest.mark.parametrize('list_defaults', util.max_results_and_next_token())
def test_logs_list(parser, client, w_id, we_id, t_id, te_id, list_defaults):
    args = [
        'logs',
        'list',
        *w_id,
        *t_id,
        *we_id,
        *te_id,
        *list_defaults,
    ]
    util.main_parser(parser, client, args)


def test_logs_get(parser, client):
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr('base64.b64decode', lambda *args: b'foo')
        args = [
            'logs',
            'get',
            service.create_log_id(),
        ]
        util.main_parser(parser, client, args)
