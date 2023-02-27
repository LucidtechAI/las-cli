import json
import pytest
from tests import service, util


@pytest.mark.parametrize('sort_by', [('--sort-by', 'createdTime')])
@pytest.mark.parametrize('order', [('--order', 'ascending'), ('--order', 'descending')])
def test_predictions_list(parser, client, list_defaults, sort_by, order):
    args = [
        'predictions',
        'list',
        *list_defaults,
        *sort_by,
        *order,
    ]
    util.main_parser(parser, client, args)


@pytest.mark.parametrize('rotation', [['--rotation', '90'], []])
@pytest.mark.parametrize('auto_rotate', [['--auto-rotate'], []])
@pytest.mark.parametrize('max_pages', [['--max-pages', '3'], []])
@pytest.mark.parametrize('image_quality', [['--image-quality', 'HIGH'], ['--image-quality', 'LOW'], []])
@pytest.mark.parametrize('postprocess_config', [
    ['--postprocess-config', json.dumps({'strategy': 'BEST_FIRST'})],
    [],
])
def test_predictions_create(parser, client, auto_rotate, max_pages, image_quality, postprocess_config, rotation):
    args = [
        'predictions',
        'create',
        service.create_document_id(),
        service.create_model_id(),
        *auto_rotate,
        *image_quality,
        *max_pages,
        *postprocess_config,
        *rotation,
    ]
    util.main_parser(parser, client, args)
