import json
import pytest
from tests import service, util


@pytest.mark.parametrize('sort_by', [('--sort-by', 'createdTime')])
@pytest.mark.parametrize('order', [('--order', 'ascending'), ('--order', 'descending')])
@pytest.mark.parametrize('model_id', [('--model-id', service.create_model_id())])
def test_predictions_list(parser, client, list_defaults, sort_by, order, model_id):
    args = [
        'predictions',
        'list',
        *list_defaults,
        *sort_by,
        *order,
        *model_id,
    ]
    util.main_parser(parser, client, args)


@pytest.mark.parametrize('preprocess_config', [
    ('--preprocess-config', json.dumps({'rotation': 0, 'autoRotate': True, 'maxPages': 1, 'imageQuality': 'LOW'})),
    ('--preprocess-config', json.dumps({'rotation': 90, 'autoRotate': False, 'maxPages': 2, 'imageQuality': 'HIGH'})),
    ('--preprocess-config', json.dumps({'rotation': 180, 'maxPages': 3})),
    ('--preprocess-config', json.dumps({'rotation': 270, 'autoRotate': True, 'imageQuality': 'HIGH'})),
    ('--preprocess-config', json.dumps({'autoRotate': False, 'pages': [0, 1, -1], 'imageQuality': 'LOW'})),
    (),
])
@pytest.mark.parametrize('postprocess_config', [
    ('--postprocess-config', str(util.postprocess_config_path())),
    ('--postprocess-config', util.postprocess_config_path().read_text()),
    (),
])
def test_predictions_create(parser, client, preprocess_config, postprocess_config):
    args = [
        'predictions',
        'create',
        service.create_document_id(),
        service.create_model_id(),
        *preprocess_config,
        *postprocess_config,
    ]
    util.main_parser(parser, client, args)
