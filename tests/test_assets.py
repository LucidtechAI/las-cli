import pytest
from tests import service, util


def test_assets_create(parser, client, name_and_description):
    args = [
        'assets',
        'create',
        str(util.metadata_path()),
        *name_and_description,
    ]
    util.main_parser(parser, client, args)


@pytest.mark.parametrize('asset_path', [('--asset-path', str(util.metadata_path())), ()])
def test_assets_update(parser, client, name_and_description, asset_path):
    args = [
        'assets',
        'update',
        service.create_asset_id(),
        *name_and_description,
        *asset_path,
    ]

    if len(args) == 3:  # patch call requires at least one change
        with pytest.raises(Exception):
            util.main_parser(parser, client, args)
    else:
        util.main_parser(parser, client, args)


def test_assets_list(parser, client, list_defaults):
    args = [
        'assets',
        'list',
        *list_defaults,
    ]
    util.main_parser(parser, client, args)


@pytest.mark.parametrize('output_content', [('--output-content',), ()])
@pytest.mark.parametrize('download_content', [('--download-content', service.temporary_named_file()), ()])
def test_assets_get(parser, client, output_content, download_content):
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr('base64.b64decode', lambda *args: b'foo')
        args = [
            'assets',
            'get',
            service.create_asset_id(),
            *output_content,
            *download_content,
        ]
        util.main_parser(parser, client, args)


@pytest.mark.skip
def test_assets_delete(parser, client):
    args = [
        'assets',
        'delete',
        service.create_asset_id(),
    ]
    util.main_parser(parser, client, args)
