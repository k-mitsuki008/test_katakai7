import json
from importlib import import_module, reload

from common.error.not_expected_error import NotExpectedError

from tests.test_utils.utils import get_event

module = import_module('src.functions.route_list.get_handler')
get_handler = getattr(module, 'handler')


def test_handler_ok_01(mocker):
    """
    正常系 ルート一覧取得API
    """
    event = get_event(gigya_uid='test_uid_02', path='/route')

    context = {}

    # service.route_service.get_route_listのモック化
    mocker.patch(
        'service.route_service.get_route_list',
        return_value=[
            {
                "route_id": 2,
                "user_vehicle_id": 2,
                "save_timestamp": "2023-09-12 11:27:46.642000",
                "destination_name": "虎ノ門ヒルズ森タワー",
                "latitude": 35.667009003,
                "longitude": 139.749387112,
                "destination_place_id": "ChIJdc0fopOLGGARm4DVQaWiPZ0",
                "ride_date": "2023-10-02",
                "weather": "001",
                "weather_icon": "001",
                "duration": 200,
                "distance": 200
            }
        ]
    )

    reload(module)

    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch('common.rds.connect.DbConnection.connect', return_value={None})

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "routes": [
            {
                "route_id": 2,
                "user_vehicle_id": 2,
                "save_timestamp": "2023-09-12 11:27:46.642000",
                "destination_name": "虎ノ門ヒルズ森タワー",
                "latitude": 35.667009003,
                "longitude": 139.749387112,
                "destination_place_id": "ChIJdc0fopOLGGARm4DVQaWiPZ0",
                "ride_date": "2023-10-02",
                "weather": "001",
                "weather_icon": "001",
                "duration": 200,
                "distance": 200
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
    正常系 ルート一覧取得API
    取得件数：0件
    """
    event = get_event(gigya_uid='test_uid_09', path='/route')

    context = {}

    # service.route_service.get_route_listのモック化
    mocker.patch(
        'service.route_service.get_route_list',
        return_value=[]
    )

    reload(module)

    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch('common.rds.connect.DbConnection.connect', return_value={None})

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "routes": []
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ng_01(mocker):
    """
    異常系 ルート一覧取得API
    """
    event = get_event(gigya_uid='test_uid_02', path='/route')

    context = {}

    # service.route_service.get_route_listのモック化
    mocker.patch(
        'service.route_service.get_route_list',
        side_effect=NotExpectedError()
    )

    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch('common.rds.connect.DbConnection.connect', return_value={None})

    reload(module)

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
