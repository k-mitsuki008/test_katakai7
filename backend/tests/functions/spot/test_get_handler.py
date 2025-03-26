import json
from importlib import import_module, reload

import pytest
from common.error.not_expected_error import NotExpectedError
from tests.test_utils.utils import get_event

module = import_module('src.functions.spot.get_handler')
get_handler = getattr(module, 'handler')


def test_handler_ok_01(mocker):
    """
    正常系 スポット取得API
    リクエスト.半径の設定あり
    """
    event = get_event(
        query_string_parameters={'latitude': '35', 'longitude': '135', 'radius': '100'},
        gigya_uid='test_uid_02', path='/spot')

    context = {}

    # service.spot_service.get_spotのモック化
    mocker.patch(
        'service.spot_service.get_spot',
        return_value=[
            {
                "spot_id": 1,
                "spot_type_code": "00001",
                "latitude": 35.686178921,
                "longitude": 139.70299927,
                "rechargeable_flag": True
            }
        ]
    )

    reload(module)

    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch('common.rds.connect.DbConnection.connect', return_value={None})

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "spots": [
            {
                "spot_id": 1,
                "spot_type_code": "00001",
                "latitude": 35.686178921,
                "longitude": 139.70299927,
                "rechargeable_flag": True
            }
        ]
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_02(mocker):
    """
    正常系 スポット取得API
    リクエスト.半径の設定なし
    """
    event = get_event(
        query_string_parameters={'latitude': '35', 'longitude': '135'}, gigya_uid='test_uid_02', path='/spot')

    context = {}

    # service.spot_service.get_spotのモック化
    mocker.patch(
        'service.spot_service.get_spot',
        return_value=[
            {
                "spot_id": 1,
                "spot_type_code": "00001",
                "latitude": 35.686178921,
                "longitude": 139.70299927,
                "rechargeable_flag": True
            }
        ]
    )

    reload(module)

    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch('common.rds.connect.DbConnection.connect', return_value={None})

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "spots": [
            {
                "spot_id": 1,
                "spot_type_code": "00001",
                "latitude": 35.686178921,
                "longitude": 139.70299927,
                "rechargeable_flag": True
            }
        ]
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ng_01(mocker):
    """
    異常系 スポット取得API
    """
    event = get_event(
        query_string_parameters={'latitude': '35', 'longitude': '135'}, gigya_uid='test_uid_02', path='/spot')

    context = {}

    # service.spot_service.get_spotのモック化
    mocker.patch(
        'service.spot_service.get_spot',
        side_effect=NotExpectedError()
    )

    reload(module)

    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch('common.rds.connect.DbConnection.connect', return_value={None})

    # 期待しているレスポンスボディの値
    expected_value = {
        'errors': {'code': 'E001',
                   'message': 'システムエラーが発生しました。\n時間をあけて再度操作をお願いいたします。',
                   'validationErrors': None},
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 500
    assert body == expected_value


@pytest.mark.parametrize(
    ['latitude', 'longitude', 'radius', 'error_value_name', 'error_code', 'error_message'],
    [
        (None, '130.0', None, 'latitude', 'E006', 'missing field'),
        ('35.0', None, None, 'longitude', 'E006', 'missing field'),
        ('a', '135.0', '100', 'latitude', 'E007', 'validation error'),
        ('35.0', 'a', '100', 'longitude', 'E007', 'validation error'),
        ('35.0', '135.0', 'a', 'radius', 'E007', 'validation error'),
        ('35.0', '130.0', '100.0', 'radius', 'E007', 'validation error')
    ]
)
def test_handler_ng_2(mocker, latitude, longitude, radius, error_value_name, error_code, error_message):
    """
    異常系 バリデーションエラー
    """
    request = {'latitude': latitude, 'longitude': longitude, 'radius': radius}

    # リクエスト項目が None の場合は辞書から要素を削除する
    if latitude is None:
        del request['latitude']
    if longitude is None:
        del request['longitude']
    if radius is None:
        del request['radius']

    event = get_event(query_string_parameters=request, gigya_uid='test_uid_02', path='/spot')

    context = {}

    reload(module)

    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch('common.rds.connect.DbConnection.connect', return_value={None})

    # 期待しているレスポンスボディの値
    expected_value = {
        'errors': {
            'code': 'E005', 'message': 'validation error',
            'validationErrors': [
                {
                    'code': error_code,
                    'field': error_value_name,
                    'message': error_message
                }
            ]
        }
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value
