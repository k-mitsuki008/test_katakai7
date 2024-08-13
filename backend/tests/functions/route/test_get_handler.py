import json
from importlib import import_module, reload

from common.error.business_error import BusinessError

from tests.test_utils.utils import get_event

module = import_module('src.functions.route.get_handler')
get_handler = getattr(module, 'handler')


def test_handler_ok_01(mocker):
    """
    正常系 ルート一覧取得API
    """
    event = get_event(gigya_uid='test_uid_03', path='/route/{route_id}', path_parameters={
        'route_id': '123'
    })

    context = {}

    # service.route_service.get_routeのモック化
    mocker.patch(
        'service.route_service.get_route',
        return_value={
            'route_id': 5,
            'user_vehicle_id': 2,
            'save_timestamp': '2023-09-12 11:27:46.642000',
            'origin_name': '虎ノ門ヒルズ森タワー',
            'origin_latitude': 35.667009003,
            'origin_longitude': 139.749387112,
            'origin_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
            'destination_name': '虎ノ門ヒルズ森タワー',
            'destination_latitude': 35.667009003,
            'destination_longitude': 139.749387112,
            'destination_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
            'ride_date': '2023-10-02',
            'weather': '001',
            'weather_icon': '001',
            'one_ways': [{
                'round_trip_type_code': '10',
                'select_flag': True,
                'duration': 123,
                'distance': 123,
                'route_type': '12',
                'route_via_points': [{
                    'latitude': 35.667009003,
                    'longitude': 139.749387112,
                    'route_via_point_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0'
                }, {
                    'latitude': 35.667009003,
                    'longitude': 139.749387112,
                    'route_via_point_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0'
                }]
            }],
            'bicycle_parking': [{
                'bicycle_parking_name': 'テスト駐輪場',
                'bicycle_parking_distance': 100,
                'latitude': 35.667009003,
                'longitude': 139.749387112,
                'bicycle_parking_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0'
            }, {
                'bicycle_parking_name': 'テスト駐輪場',
                'bicycle_parking_distance': 100,
                'latitude': 35.667009003,
                'longitude': 139.749387112,
                'bicycle_parking_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0'
            }]
        }
    )

    reload(module)

    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch('common.rds.connect.DbConnection.connect', return_value={None})

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        'route_id': 5,
        'user_vehicle_id': 2,
        'save_timestamp': '2023-09-12 11:27:46.642000',
        'origin_name': '虎ノ門ヒルズ森タワー',
        'origin_latitude': 35.667009003,
        'origin_longitude': 139.749387112,
        'origin_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
        'destination_name': '虎ノ門ヒルズ森タワー',
        'destination_latitude': 35.667009003,
        'destination_longitude': 139.749387112,
        'destination_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
        'ride_date': '2023-10-02',
        'weather': '001',
        'weather_icon': '001',
        'one_ways': [{
            'round_trip_type_code': '10',
            'select_flag': True,
            'duration': 123,
            'distance': 123,
            'route_type': '12',
            'route_via_points': [{
                'latitude': 35.667009003,
                'longitude': 139.749387112,
                'route_via_point_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0'
            }, {
                'latitude': 35.667009003,
                'longitude': 139.749387112,
                'route_via_point_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0'
            }]
        }],
        'bicycle_parking': [{
            'bicycle_parking_name': 'テスト駐輪場',
            'bicycle_parking_distance': 100,
            'latitude': 35.667009003,
            'longitude': 139.749387112,
            'bicycle_parking_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0'
        }, {
            'bicycle_parking_name': 'テスト駐輪場',
            'bicycle_parking_distance': 100,
            'latitude': 35.667009003,
            'longitude': 139.749387112,
            'bicycle_parking_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0'
        }]
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
    event = get_event(gigya_uid='test_uid_02', path='/route/{route_id}', path_parameters={
        'route_id': '123'
    })

    context = {}

    # service.route_service.get_route_listのモック化
    mocker.patch(
        'service.route_service.get_route',
        side_effect=BusinessError()
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

    assert status_code == 400
    assert body == expected_value
