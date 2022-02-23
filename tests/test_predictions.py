import json
import pytest
from tests import service, util


def test_predictions_list(parser, client, list_defaults):
    args = [
        'predictions',
        'list',
        *list_defaults,
    ]
    util.main_parser(parser, client, args)


@pytest.mark.parametrize('auto_rotate', [['--auto-rotate'], []])
@pytest.mark.parametrize('max_pages', [['--max-pages', '3'], []])
@pytest.mark.parametrize('image_quality', [['--image-quality', 'HIGH'], ['--image-quality', 'LOW'], []])
@pytest.mark.parametrize('postprocess_config', [
    ['--postprocess-config', json.dumps({'strategy': 'BEST_FIRST'})],
    [],
])
def test_predictions_get(parser, client, auto_rotate, max_pages, image_quality, postprocess_config):
    args = [
        'predictions',
        'create',
        service.create_document_id(),
        service.create_model_id(),
        *auto_rotate,
        *max_pages,
        *image_quality,
        *postprocess_config,
    ]
    util.main_parser(parser, client, args)
